from pathlib import Path
import pandas as pd

from config.system.pipeline import (
    PARQUET_COMPRESSION, 
    PARQUET_ENGINE, 
    PARQUET_INDEX
    )

def save_parquet(dataset: pd.DataFrame, path: Path) -> None:

    dataset.to_parquet(
    path=path,
    engine=PARQUET_ENGINE,
    compression=PARQUET_COMPRESSION,
    index=PARQUET_INDEX
)
