from pathlib import Path

# Requests
HTTP_TIMEOUT = 30
HTTP_RETRIES = 2

# Parquet
PARQUET_COMPRESSION = 'snappy'
PARQUET_ENGINE = 'pyarrow'
PARQUET_INDEX = False

# Logging
LOG_LEVEL = "INFO"

# Root directory path 
BASE_DIR                = Path(__file__).parent.parent.parent.parent
DATA_DIR                = BASE_DIR / 'data'


