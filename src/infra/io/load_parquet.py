from pathlib import Path
import pandas as pd

def load_parquet(path: Path) -> None:
    return pd.read_parquet(path=path)