from pathlib import Path
import pandas as pd


def main():
    # Project root
    project_root = Path(__file__).resolve().parents[1]

    # Input file
    input_file = project_root / "data" / "raw" / "5G_millisecond.csv"

    # Output folder
    output_folder = project_root / "data" / "filtered"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(input_file, sep=";")   

    # Input Features
    df = df[['mac_dl_cqi', 'mac_dl_mcs', 'mac_dl_ok', 'mac_dl_nok',
             'mac_dl_brate', 'label', 'mob_pattern', 'ue_ident']]

    filter_pairs = [
    ("youtube", "static"),
    ("Web Browsing", "train")
]

    for label, mob in filter_pairs:
        df_filtered = df[(df["label"] == label) & (df["mob_pattern"] == mob)].copy()

        if df_filtered.empty:
            print(f"Skipping {label} + {mob}: no rows found")
            continue

        df_filtered = df_filtered.drop(columns=["label", "mob_pattern"])

        start_time = pd.Timestamp("2022-01-01 00:00:00")
        n_rows = len(df_filtered)
        new_timestamps = pd.date_range(start=start_time, periods=n_rows, freq="1ms")

        df_filtered["DATE"] = new_timestamps
        df_filtered = df_filtered.set_index("DATE")

        output_file = output_folder / f"{label}_{mob}.csv"
        df_filtered.to_csv(output_file)

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()