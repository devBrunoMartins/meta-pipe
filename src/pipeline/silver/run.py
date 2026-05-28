from core.versioning.versions_manager import get_path_by_version
from config.system.pipeline import DATA_DIR
from pipeline.silver.transform.dataframe import to_dataframe
from core.io.load_json import load_json
from pipeline.silver.transform.convert_dtypes import convert_types
from pipeline.silver.transform.rename import columns_rename
from pipeline.silver.transform.remove_nulls import remove_nulls
from pprint import pprint

def run(config: list[dict]):

    version = 'latest'    

    dataset_paths = get_path_by_version(version, DATA_DIR)

    for ds_config in config:
   
        name = ds_config['name']
        columns = ds_config['columns']
        columns_not_null = ds_config['constraints']['not_null']

        print(f'Carregando versão {version} do dataset {ds_config['label']} \nsource: \033[36m{dataset_paths[name]}\033[0m')
    
        json_dataset = load_json(dataset_paths[name])
        
        print(f'Gerando DataFrame...')

        df_dataset = to_dataframe(json_dataset, ds_config)

        print(f'Renomeando colunas...')

        df_dataset = columns_rename(df_dataset, columns)

        print(f'Convertendo os tipos de dados...')

        df_dataset = convert_types(df_dataset, ds_config['dtypes'])

        print(f'Removendo linhas com dados obrigatórios que estão nulos...')
        df_dataset = remove_nulls(df_dataset, columns_not_null)

        # print(f'Removendo linhas duplicadas...')
        # df_municipios = remove_duplicates(df_municipios, municipios_config)
        
        # dataset_name = 'dim_municipios'
        # write_dataset(df_municipios, dataset_name)
    
    print()




if __name__=='__main__':
    from config.datasets.municipios import MUNICIPIOS_CONFIG
    from config.datasets.populacao import POPULACAO_CONFIG
    from config.datasets.pib import PIB_CONFIG


    config = [
        PIB_CONFIG, 
        POPULACAO_CONFIG, 
        MUNICIPIOS_CONFIG
        ]
    # pprint(config)
    run(config=config)