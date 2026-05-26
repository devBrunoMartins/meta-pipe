from pathlib import Path
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

def build_table_versions(layer_ref: str) -> pd.DataFrame:
    path = Path(__file__).parent.parent / 'data'
        
    rows = []

    for file_path in path.rglob('*.*'):
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
    dataframe = pd.DataFrame(rows)

    dataframe = dataframe[dataframe['layer'] == layer_ref]

    return dataframe


def get_path_by_version(version: str|None = 'latest', versions_table: pd.DataFrame = None) -> dict[str: Path]:

    if version == 'latest':

        versions = (versions_table.
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


def load_path_versions(layer: str, version: str = 'latest') -> dict:

    versions_table = build_table_versions(layer_ref='silver')
    
    paths_versions = get_path_by_version(
        version=version,
        versions_table=versions_table)

    return paths_versions


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_parquet(path=path)
    




def build_gold_municipios_indicadores(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]
    fact_pib = fact_pib[columns['fact_pib']]

    municipios_indicadores = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
        .merge(
            fact_populacao,
            on='city_id',
            how='left'
            )
    )
    
    municipios_indicadores['pib_per_capita'] = municipios_indicadores['pib'] / municipios_indicadores['population']

    return municipios_indicadores.reset_index()


def build_gold_estados_resumo(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios  = dim_municipios[columns['dim_municipios']]
    fact_populacao  = fact_populacao[columns['fact_populacao']]
    fact_pib        = fact_pib[columns['fact_pib']]

    estados_resumo = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
        .merge(
            fact_populacao,
            on='city_id',
            how='left'
            )
    )

    estados_resumo = (
        estados_resumo
        .groupby(['state_id', 'state_name', 'state_sigla'])
        .agg(
            total_populacao=('population', 'sum'),
            total_pib=('pib', 'sum'),
            total_cities=('city_id', 'count')
        )
        .reset_index()

    )

    estados_resumo['avg_pib_per_capita'] = estados_resumo['total_pib'] / estados_resumo['total_populacao']

    return estados_resumo


def build_gold_ranking_pib(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_pib = fact_pib[columns['fact_pib']]

    ranking_pib = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
    )
  
    ranking_pib = ranking_pib.sort_values(['pib'], ascending=False).reset_index()

    return ranking_pib


def build_gold_ranking_populacao(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao       = datasets['fact_populacao']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]

    ranking_populacao = (
        
        dim_municipios

        .merge(
            fact_populacao,
            on='city_id',
            how='left'
               )
    )
  
    ranking_populacao = ranking_populacao.sort_values(['population'], ascending=False).reset_index()

    return ranking_populacao


def build_gold_ranking_pib_per_capita(datasets: dict[str, pd.DataFrame], columns=None) -> pd.DataFrame:
    dim_municipios  = datasets['dim_municipios']
    fact_populacao  = datasets['fact_populacao']
    fact_pib        = datasets['fact_pib']

    dim_municipios = dim_municipios[columns['dim_municipios']]
    fact_populacao = fact_populacao[columns['fact_populacao']]
    fact_pib = fact_pib[columns['fact_pib']]

    ranking_pib_per_capita = (
        
        dim_municipios

        .merge(
            fact_pib,
            on='city_id',
            how='left'
               )
        .merge(
            fact_populacao,
            on='city_id',
            how='left'
            )
    )
    
    ranking_pib_per_capita['pib_per_capita'] = ranking_pib_per_capita['pib'] / ranking_pib_per_capita['population']

    ranking_pib_per_capita = (
        ranking_pib_per_capita
        .sort_values(['pib'], ascending=False)
        .reset_index())


    return ranking_pib_per_capita


def ensure_dir(path: Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def path(dataset_name: str):

    BASE_DIR=Path(__file__).parent.parent / 'data'
    STAMP_START_PIPE=datetime.now(ZoneInfo("America/Sao_Paulo"))

    path = (f"{BASE_DIR}/"
    f"layer=gold/"
    f"dataset={dataset_name}/"
    f"year={STAMP_START_PIPE.year}/"
    f"month={STAMP_START_PIPE.month}/"
    f"day={STAMP_START_PIPE.day}/"
    f"{int(STAMP_START_PIPE.timestamp())}.parquet")

    path = Path(path)

    ensure_dir(path)

    return path


def write_dataset(dataset: pd.DataFrame, dataset_name: str) -> None:
    rote=path(dataset_name)

    dataset.to_parquet(
    path=rote,
    engine='pyarrow',
    compression='snappy',
    index=False
)
    print(f'Salvo em: \033[36m{str(rote)}\033[0m')


def run():
    
    versions = load_path_versions('silver', 'latest')
    
    dim_municipios = load_dataset(path=versions['dim_municipios'])

    fact_pib = load_dataset(path=versions['fact_pib'])
    
    fact_populacao = load_dataset(path=versions['fact_populacao'])




    ### [01] gold_municipios_indicadores
    
    print(f'Calculando Indicadores dos Municípios...')

    columns_municipio_indicadores = {
        'dim_municipios': [
            'city_id',
            'city_name',
            'microregion_name',
            'mesoregion_name',
            'state_sigla',
            'state_name'            
        ],
        'fact_populacao': [
            'city_id',
            'population'
        ],
        'fact_pib': [
            'city_id',
            'year',
            'pib'
        ]
    }
    df_gold_municipios_indicadores = build_gold_municipios_indicadores(datasets={
        'dim_municipios': dim_municipios,
        'fact_pib': fact_pib,
        'fact_populacao': fact_populacao
    },
    columns=columns_municipio_indicadores)

    write_dataset(df_gold_municipios_indicadores, 'gold_municipios_indicadores')


    ### [02] gold_estados_resumo

    print(f'Calculando Resumo dos dados por estado...')

    columns_estados_resumo = {
        'dim_municipios': [
            'city_id',
            'state_id',
            'state_name',
            'state_sigla'
        ],
        'fact_populacao': [
            'city_id',
            'population'
        ],
        'fact_pib': [
            'city_id',
            'year',
            'pib'
        ]
    }

    df_gold_estados_resumo = build_gold_estados_resumo(datasets={
        'dim_municipios': dim_municipios,
        'fact_pib': fact_pib,
        'fact_populacao': fact_populacao
    },
    columns=columns_estados_resumo)[
        ['state_id', 
         'state_name', 
         'state_sigla', 
         'total_populacao', 
         'total_pib', 
         'avg_pib_per_capita', 
         'total_cities'
         ]]
    
    write_dataset(df_gold_estados_resumo, 'gold_estados_resumo')


    ### [03] gold_ranking_pib

    print(f'Calculando ranking inter-municipal baseado no PIB...')

    columns_ranking_pib = {
        'dim_municipios': [
            'city_id',
            'city_name',
            'state_sigla'
        ],
        'fact_pib': [
            'city_id',
            'year',
            'pib'
        ]
    }
    df_gold_ranking_pib = build_gold_ranking_pib(datasets={
        'dim_municipios': dim_municipios,
        'fact_pib': fact_pib,
    },
    columns=columns_ranking_pib)

    write_dataset(df_gold_ranking_pib, 'gold_ranking_pib')



    ### [04] gold_ranking_populacao

    print(f'Calculando ranking inter-municipal baseado no PIB PER CAPTA...')

    columns_ranking_populacao = {
        'dim_municipios': [
            'city_id',
            'city_name',
            'state_sigla'
        ],
        'fact_populacao': [
            'city_id',
            'year',
            'population'
        ]
    }
    df_gold_ranking_populacao = build_gold_ranking_populacao(datasets={
        'dim_municipios': dim_municipios,
        'fact_populacao': fact_populacao,
    },
    columns=columns_ranking_populacao)

    write_dataset(df_gold_ranking_populacao, 'gold_ranking_populacao')



    ### [05] gold_ranking_pib_per_capita

    print(f'Calculando ranking cidades baseado no PIB')

    columns_ranking_pib_per_capita = {
        'dim_municipios': [
            'city_id',
            'city_name',
            'state_sigla'
        ],
        'fact_populacao': [
            'city_id',
            'population'
        ],
        'fact_pib': [
            'city_id',
            'year',
            'pib'
        ]
    }
    df_gold_ranking_pib_per_capita = build_gold_ranking_pib_per_capita(datasets={
        'dim_municipios': dim_municipios,
        'fact_populacao': fact_populacao,
        'fact_pib': fact_pib,
    },
    columns=columns_ranking_pib_per_capita)

    write_dataset(df_gold_ranking_pib_per_capita, 'gold_ranking_pib_per_capita')




if __name__ == "__main__":
    run()
