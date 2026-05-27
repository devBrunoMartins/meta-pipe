from typing import Any
import pandas as pd
import json


def to_dataframe(dataset: json, columns_config: list[dict[str, Any]]) -> pd.DataFrame:
    
    target_columns = columns_config.keys()
    
    source_columns = [
        columns_config[key]['source']
        for key in target_columns
        ]
    
    column_map = dict(zip(source_columns, target_columns))

    dataframe = (
        pd.json_normalize(dataset)
        [column_map.keys()].
        rename(columns=column_map)
    )

    return dataframe