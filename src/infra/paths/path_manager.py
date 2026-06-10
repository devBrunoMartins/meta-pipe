from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def ensure_path(path: Path):
        path.mkdir(
        parents=True,
        exist_ok=True
    )


def remove_files(paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            path.unlink()


def prepare_path(
    dataset: str,
    data_dir: Path,
    layer: str,
    extension: str
) -> Path:

    timestamp = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )
    file_name = str(timestamp.timestamp()).replace('.', '_')
    path = (
        data_dir
        / f"layer={layer}"
        / f"dataset={dataset}"
        / f"year={timestamp.year}"
        / f"month={timestamp.month:02d}"
        / f"day={timestamp.day:02d}"
        / f"{file_name}.{extension}"
    )

    ensure_path(path.parent)

    return path


if __name__=='__main__':
    ...