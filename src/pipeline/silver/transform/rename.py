import pandas as pd

def columns_rename(
        dataset: pd.DataFrame,
        columns_config: list[dict[str, list | str]]
        ) -> pd.DataFrame:

    sources_raw = [
        column['source']
        for column in columns_config
    ]

    sources_str = []
    for column in sources_raw:
        column_str = ".".join(column)
        sources_str.append(column_str)

    targets = [
        column['target']
        for column in columns_config
    ]

    titles_map = dict(zip(sources_str, targets))

    dataset = (
        dataset
        .rename(columns=titles_map)
    )

    return dataset