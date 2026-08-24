from pathlib import Path
import argparse
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from river import preprocessing, forest


def load_data(project_root: Path, dataset_name: str) -> pd.DataFrame:
    data_file = project_root / "data" / "filtered" / dataset_name
    if not data_file.exists():
        raise FileNotFoundError(
            f"Could not find dataset: {data_file}\n"
            f"Make sure the filtered CSV exists in data/filtered/."
        )

    df = pd.read_csv(data_file, parse_dates=["DATE"], index_col="DATE")
    return df


def build_model(seed: int):
    return preprocessing.StandardScaler() | forest.ARFRegressor(
        seed=seed
    )

print('Model Training started....')
def train_and_evaluate(df: pd.DataFrame, horizon: int, seed: int):
    split_point = int(len(df) * 0.8)
    test_start_time = df.index[split_point]

    model = build_model(seed)

    records = []

    feature_cols = [col for col in df.columns if col not in ["mac_dl_brate", "ue_ident"]]

    for t in range(horizon, len(df) - horizon):
        # Prediction step
        if df.index[t] >= test_start_time:
            start_pred = time.time()

        for h in range(1, horizon + 1):
            idx = t + h
            row = df.iloc[idx]
            x = {col: row[col] for col in feature_cols}
            pred = model.predict_one(x)
            actual = row["mac_dl_brate"]
            timestamp = df.index[idx]
            source_t = df.index[t]

            records.append(
                {
                    "timestamp": timestamp,
                    "source_t": source_t,
                    "horizon": h,
                    "actual": actual,
                    "prediction": pred,
                    "seed": seed,
                }
            )


        # Training step
        if df.index[t + 1] < test_start_time:
            row = df.iloc[t + 1]
            x = {col: row[col] for col in feature_cols}
            y = row["mac_dl_brate"]
            model.learn_one(x, y)

    df_forecasts = pd.DataFrame(records)
    df_test_forecasts = df_forecasts[df_forecasts["source_t"] >= test_start_time].copy()

    train_actuals = df_forecasts[df_forecasts["source_t"] < test_start_time]["actual"]
    scaler = MinMaxScaler()
    scaler.fit(train_actuals.values.reshape(-1, 1))

    actual_scaled = scaler.transform(df_test_forecasts["actual"].values.reshape(-1, 1)).flatten()
    pred_scaled = scaler.transform(df_test_forecasts["prediction"].values.reshape(-1, 1)).flatten()

    rmse = float(np.sqrt(mean_squared_error(actual_scaled, pred_scaled)))
    mae = float(mean_absolute_error(actual_scaled, pred_scaled))

    metrics_dict = {
        "seed": seed,
        "horizon": horizon,
        "split_point": split_point,
        "test_start_time": str(test_start_time),
        "scaled_rmse": rmse,
        "scaled_mae": mae,
    }

    return df_forecasts, df_test_forecasts, metrics_dict, test_start_time
    
def save_plot(df_test_forecasts: pd.DataFrame, rmse: float, mae: float, output_path: Path):
    df_agg = (
        df_test_forecasts.groupby("source_t").agg({"actual": "mean", "prediction": "mean"}).dropna().reset_index()
    )
    df_agg["source_t"] = pd.to_datetime(df_agg["source_t"])

    plt.figure(figsize=(10, 6))
    plt.plot(df_agg["source_t"], df_agg["actual"], label="Actual")
    plt.plot(df_agg["source_t"], df_agg["prediction"], label="Predicted")
    plt.title(f"Adaptive Random Forest\nRMSE: {rmse:.4f}, MAE: {mae:.4f}")
    plt.xlabel("Timestamp")
    plt.ylabel("Downlink Bitrate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Run Adaptive Random Forest on a filtered time-series dataset.")
    parser.add_argument("--dataset", default="webbrowsing_train.csv", help="CSV file inside data/filtered/")
    parser.add_argument("--horizon", type=int, default=96, help="Forecast horizon")
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[42],
        help="List of random seeds to evaluate",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    results_dir = (project_root/ "notebooks"/ "results"/ "metrics"/ "web_browsing")
    results_dir.mkdir(parents=True, exist_ok=True)

    dataset_stem = Path(args.dataset).stem
    df = load_data(project_root, args.dataset)

    df = df[['mac_dl_brate']]

    target = 'mac_dl_brate'

    num_lags = 2
    for lag in range(1, num_lags + 1):
        df[f'{target}_lag_{lag}'] = df[target].shift(lag)

    df.dropna(inplace=True)

    print(f"Loaded dataset: {args.dataset}")
    print(f"Shape: {df.shape}")

    all_metrics = []
    all_test_forecasts = []

    for seed in args.seeds:
        print(f"\nRunning ARF with seed {seed}...")
        df_forecasts, df_test_forecasts, metrics_dict, _ = train_and_evaluate(df, args.horizon, seed)

        all_metrics.append(metrics_dict)
        all_test_forecasts.append(df_test_forecasts)

        print(f"Seed {seed} -> RMSE: {metrics_dict['scaled_rmse']:.4f}, MAE: {metrics_dict['scaled_mae']:.4f}")

    metrics_df = pd.DataFrame(all_metrics)
    metrics_file = results_dir / f"arf_uni_metrics.csv"
    metrics_df.to_csv(metrics_file, index=False)
    print(f"\nSaved metrics: {metrics_file}")

    summary = {
        "dataset": dataset_stem,
        "horizon": args.horizon,
        "seeds": ",".join(map(str, args.seeds)),
        "mean_scaled_rmse": metrics_df["scaled_rmse"].mean(),
        "std_scaled_rmse": metrics_df["scaled_rmse"].std(ddof=0),
        "mean_scaled_mae": metrics_df["scaled_mae"].mean(),
        "std_scaled_mae": metrics_df["scaled_mae"].std(ddof=0)
    }
    summary_df = pd.DataFrame([summary])
    summary_file = results_dir / f"arf_uni_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    print(f"Saved summary: {summary_file}")

    print("\nSummary")
    print(f"RMSE: {summary['mean_scaled_rmse']:.4f} ± {summary['std_scaled_rmse']:.4f}")
    print(f"MAE : {summary['mean_scaled_mae']:.4f} ± {summary['std_scaled_mae']:.4f}")


if __name__ == "__main__":
    main()



