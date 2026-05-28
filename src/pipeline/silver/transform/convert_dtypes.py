from typing import Any
import pandas as pd


def convert_types(
        dataset: pd.DataFrame,
        columns_config: dict[str, dict[str, Any]]
        ) -> pd.DataFrame:


    numeric_dtypes = [
        'Int8', 'Int16', 'Int32', 'Int64',
        'UInt8', 'UInt16', 'UInt32', 'UInt64',
        'Float32', 'Float64'
    ]

    string_dtypes = ['string']

    boolean_dtypes = ['boolean']

    datetime_dtypes = [
        'datetime64[ns]',
        'datetime64[ns, UTC]'
    ]

    timedelta_dtypes = ['timedelta64[ns]']

    category_dtypes = ['category']

    for column, dtype in columns_config.items():

        # NUMÉRICOS
        if dtype in numeric_dtypes:

            dataset[column] = (
                pd.to_numeric(dataset[column], errors='coerce')
                .astype(dtype)
            )

        # STRING
        elif dtype in string_dtypes:

            dataset[column] = (
                dataset[column]
                .astype('string')
                .str.strip()
            )

        # BOOLEAN
        elif dtype in boolean_dtypes:

            dataset[column] = (
                dataset[column]
                .astype('boolean')
            )

        # DATETIME
        elif dtype in datetime_dtypes:

            dataset[column] = (
                pd.to_datetime(dataset[column], errors='coerce')
            )

        # TIMEDELTA
        elif dtype in timedelta_dtypes:

            dataset[column] = (
                pd.to_timedelta(dataset[column], errors='coerce')
            )

        # CATEGORY
        elif dtype in category_dtypes:

            dataset[column] = (
                dataset[column]
                .astype('category')
            )

        # FALLBACK
        else:

            dataset[column] = (
                dataset[column]
                .astype(dtype)
            )

    return dataset