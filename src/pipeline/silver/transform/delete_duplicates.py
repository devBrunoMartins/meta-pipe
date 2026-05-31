import pandas as pd


def delete_duplicates(dataset: pd.DataFrame, columns_unique: list[str]) -> pd.DataFrame:
    
    if columns_unique:
        dataset = dataset.drop_duplicates(subset=columns_unique)
    else:
        dataset = dataset.drop_duplicates()

    return dataset