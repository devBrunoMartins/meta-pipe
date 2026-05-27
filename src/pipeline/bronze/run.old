import  requests
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


def ingest_data(url: str) -> list:
    
    # Obtém dados da api
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Remove header do SIDRA
    is_sidra_header = (
        isinstance(data, list)
        and data
        and isinstance(data[0], dict)
        and data[0].get('V') == 'Valor'
    )

    if is_sidra_header:
        return data[1:]

    # Normaliza dataset de população
    is_population_dataset = (
        isinstance(data, list)
        and data
        and isinstance(data[0], dict)
        and 'resultados' in data[0]
    )

    if is_population_dataset:

        series = data[0]['resultados'][0]['series']

        normalized = []

        for item in series:

            year, population = next(
                iter(item['serie'].items())
            )

            normalized.append({
                'localidade': item['localidade'],
                'year': int(year),
                'population': int(population)
            })

        return normalized

    return data
    

def build_path(path_str: str) -> Path:
    Path(Path(path_str)).parent.mkdir(parents=True, exist_ok=True)

    return Path(path_str)


def save(data: list, path: Path) -> bool:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    if Path(path).exists() and Path(path).is_file:
        return True

    return False


def run(production: bool=True) -> None:

    BASE_DIR=Path(__file__).parent.parent / 'data'
    STAMP_START_PIPE=datetime.now(ZoneInfo("America/Sao_Paulo"))
    DATASETS = {
       'municipios' : 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios',
       'pib'        : 'https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/2021',
       'populacao'  : 'https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N6'
    }

    for dataset, url in DATASETS.items():

        path_str = (f"{BASE_DIR}/"
            f"layer=bronze/"
            f"dataset={dataset}/"
            f"year={STAMP_START_PIPE.year}/"
            f"month={STAMP_START_PIPE.month}/"
            f"day={STAMP_START_PIPE.day}/"
            f"{int(STAMP_START_PIPE.timestamp())}.json")
        
        print(f'Extraíndo \"\033[36m{dataset}\033[0m"\nURL:       \033[36m{url}\033[0m')
        path = build_path(path_str)
        data = ingest_data(url)
        
        save(data, path)
        print(f'Salvo em:  \033[36m{str(path)}\033[0m')
        

if __name__ == '__main__':
    run(production=True)