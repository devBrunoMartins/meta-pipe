from typing import Any
import pandas as pd


def _extract_payload(
        dataset: dict | list,
        payload: dict | None,
        columns_config: list[dict[str, list | str]]
        ) -> pd.DataFrame:

    source_columns = [
        column['source']
        for column in columns_config
    ]
    
    titles = []
    for column in source_columns:
        column_str = ".".join(column)
        titles.append(column_str)

    record_path = payload.get('record_path', None)

    dataset = (
        pd.json_normalize(
            data=dataset,
            record_path=record_path
            )[titles]
    )

    return dataset


def _add_static_column(
        dataset: pd.DataFrame,
        static_columns: dict[str, Any]
        ) -> pd.DataFrame:
    
    dataset = dataset.assign(
        **static_columns
    )

    return dataset


def skip_rows(
        dataset: pd.DataFrame,
        rows: int
        ) -> pd.DataFrame:
    
    dataset = dataset.iloc[rows:].reset_index(drop=True)

    return dataset


def to_dataframe(
        dataset: dict | list,
        configs: dict[str, Any]
        ) -> pd.DataFrame:
    
    columns_config = configs.get('columns')
    payload = configs.get('payload')
    if columns_config:
        dataset = _extract_payload(
            dataset=dataset,
            payload=payload,
            columns_config=columns_config
            )

    pre_processing = configs.get('pre_processing')
    if pre_processing:
        dataset = skip_rows(
            dataset=dataset,
            rows=pre_processing['skip_rows']
            )

    # Adiciona colunas estáticas
    static_columns = configs.get('static_columns')
    if static_columns:
        dataset = _add_static_column(
            dataset=dataset,
            static_columns=static_columns
            )
    
    return dataset



