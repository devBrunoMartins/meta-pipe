from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def prepare_path(
    dataset: str,
    base_root: Path,
    layer: str,
    extension: str
) -> Path:

    timestamp = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    path = (
        base_root
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
    from config.system.pipeline import BASE_DIR
    print(prepare_path(
    dataset = 'exemplo',
    base_root = BASE_DIR,
    layer = 'silver',
    extension = 'cvs'
))