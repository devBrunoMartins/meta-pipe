from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def prepare_path(
    dataset: str,
    data_dir: Path,
    layer: str,
    extension: str
) -> Path:

    timestamp = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    path = (
        data_dir
        / f"layer={layer}"
        / f"dataset={dataset}"
        / f"year={timestamp.year}"
        / f"month={timestamp.month:02d}"
        / f"day={timestamp.day:02d}"
        / f"{int(timestamp.timestamp())}.{extension}"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


if __name__=='__main__':
    ...