import pandas as pd

def remove_nulls(
        dataset: pd.DataFrame,
        columns_not_null: list | str
) -> pd.DataFrame:
    
    for column in columns_not_null:
        dataset = dataset[dataset[column].notna()]

    return dataset