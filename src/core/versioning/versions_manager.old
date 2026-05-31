import pandas as pd
from pathlib import Path

def build_table_versions(
        data_dir: Path,
) -> pd.DataFrame:
        
    rows = []

    for file_path in data_dir.rglob("*.json"):

        parts = file_path.parts
        layer = parts[-6].split('=')[1]
        dataset = parts[-5].split('=')[1]
        ano = parts[-4].split('=')[1]
        mes = parts[-3].split('=')[1]
        dia = parts[-2].split('=')[1]
        file = file_path.name

        rows.append({
            'layer': layer,
            'dataset': dataset,
            'ano': int(ano),
            'mes': int(mes),
            'dia': int(dia),
            'file': file,
            'caminho': str(file_path)
        })
   
    return pd.DataFrame(rows)


def get_path_by_version(
        version: str|None,
        data_dir: Path
        ) -> dict[str: Path]:
    
    table_versions = build_table_versions(data_dir)

    ### A busca por versões personalizadas será implementada no futuro
    ### por enquanto não funciona. e os parâmetros estão aí à toa.

    if version == 'latest':

        versions = (table_versions.
                sort_values('ano', ascending=False).
                sort_values('mes', ascending=False).
                sort_values('dia', ascending=False).
                sort_values('file', ascending=False).
                head(3))
        
    path_datasets = dict(zip(versions['dataset'], versions['caminho']))

    path_datasets = {
        k: Path(v)
        for k, v in path_datasets.items()
                     }
    
    return path_datasets



