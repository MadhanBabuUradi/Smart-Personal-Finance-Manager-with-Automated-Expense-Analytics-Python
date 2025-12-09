import pandas as pd
from pathlib import Path

def read_expenses_csv(path):
    df = pd.read_csv(path, parse_dates=['date'])
    return df

def write_csv(df, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
