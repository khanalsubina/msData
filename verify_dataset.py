from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "Network_data.csv"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print("Printing Network Dataset")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())