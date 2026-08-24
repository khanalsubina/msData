from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from river import preprocessing, linear_model, optim


def load_data(project_root: Path, dataset_name: str) -> pd.DataFrame:
    data_file = project_root / "data" / "filtered" / dataset_name
    if not data_file.exists():
        raise FileNotFoundError(
            f"Could not find dataset: {data_file}\n"
            f"Make sure the filtered CSV exists in data/filtered/."
        )

    df = pd.read_csv(data_file, parse_dates=["DATE"], index_col="DATE")
    df = df.sort_index()
    return df

print('Model Training started....')
def main():
    parser = argparse.ArgumentParser(
        description="Run Online Linear Regression on a filtered time-series dataset."
    )
    parser.add_argument(
        "--dataset",
        default="webbrowsing_train.csv",
        help="CSV file inside data/filtered/"
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=96,
        help="Forecast horizon"
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    results_dir = (project_root/ "notebooks"/ "results"/ "metrics"/ "web_browsing")
    results_dir.mkdir(parents=True, exist_ok=True)

    dataset_stem = Path(args.dataset).stem
    df = load_data(project_root, args.dataset)

    print(f"Loaded dataset: {args.dataset}")
    print(f"Shape: {df.shape}")

    # Train-test split
    n = len(df)
    train_size = int(n * 0.8)

    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    # Model
    model = (
        preprocessing.StandardScaler() |
        linear_model.LinearRegression(optimizer=optim.SGD(1e-6))
    )

    records = []
    horizon = args.horizon

    for t in range(horizon, len(df) - horizon):

        # MULTI-HORIZON PREDICTION
        for h in range(1, horizon + 1):
            idx = t + h
            row = df.iloc[idx]

            x = {col: row[col] for col in df.columns if col != 'mac_dl_brate'}
            pred = model.predict_one(x)
            actual = row['mac_dl_brate']

            records.append({
                'timestamp': df.index[idx],
                'source_t': df.index[t],
                'horizon': h,
                'actual': actual,
                'prediction': pred
            })

        # ONLINE TRAINING ON THE NEXT TRUE VALUE
        train_row = df.iloc[t + 1]
        x_train = {col: train_row[col] for col in df.columns if col != 'mac_dl_brate'}
        y_train = train_row['mac_dl_brate']

        model.learn_one(x_train, y_train)

    df_rec = pd.DataFrame(records)

    # Scaling
    scaler = MinMaxScaler()
    scaler.fit(train["mac_dl_brate"].values.reshape(-1, 1))

    actual = df_rec["actual"].values.reshape(-1, 1)
    pred = df_rec["prediction"].values.reshape(-1, 1)

    actual_scaled = scaler.transform(actual)
    pred_scaled = scaler.transform(pred)

    rmse_scaled = np.sqrt(mean_squared_error(actual_scaled, pred_scaled))
    mae_scaled = mean_absolute_error(actual_scaled, pred_scaled)

    print("Scaled RMSE:", rmse_scaled)
    print("Scaled MAE :", mae_scaled)

    # Save metrics
    metrics_df = pd.DataFrame([{
        "model": "OLR",
        "setting": "multivariate",
        "dataset": dataset_stem,
        "rmse": rmse_scaled,
        "mae": mae_scaled,
    }])

    metrics_file = results_dir / f"olr_multi_metrics.csv"
    metrics_df.to_csv(metrics_file, index=False)
    print("Saved metrics to:", metrics_file)



if __name__ == "__main__":
    main()
