from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = PROJECT_ROOT / "results" / "metrics"
OUTPUT_FILE = PROJECT_ROOT / "results" / "summary_all_models.csv"

all_files = list(METRICS_DIR.glob("*.csv"))

if not all_files:
    print("No metrics files found.")
else:
    dfs = []
    for file in all_files:
        df = pd.read_csv(file)
        df["source_file"] = file.name
        dfs.append(df)

    summary_df = pd.concat(dfs, ignore_index=True)
    summary_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved combined summary to: {OUTPUT_FILE}")