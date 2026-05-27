from pathlib import Path
import json

def save_json(data: list, path: Path) -> bool:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    if Path(path).exists() and Path(path).is_file:
        return True

    return False