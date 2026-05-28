from core.versioning.versions_manager import get_path_by_version
from config.system.pipeline import DATA_DIR
from pipeline.silver.transform.dataframe import to_dataframe
from core.io.load_json import load_json
from pipeline.silver.transform.convert_dtypes import convert_types
from pipeline.silver.transform.rename import columns_rename

from pprint import pprint

def run(config: list[dict]):

    version = 'latest'    

    dataset_paths = get_path_by_version(version, DATA_DIR)

    for ds_config in config:
   
        name = ds_config['name']
        columns = ds_config['columns']

        print(f'Carregando versão {version} do dataset {ds_config['label']} \nsource: \033[36m{dataset_paths[name]}\033[0m')
    
        json_dataset = load_json(dataset_paths[name])
        
        print(f'Gerando Pandas DataFrame...')

        df_dataset = to_dataframe(json_dataset, ds_config)

        print(f'Convertendo os tipos de dados...')

        df_dataset = to_dataframe(json_dataset, ds_config)

        df_dataset = columns_rename(df_dataset, columns)

        print(df_dataset)

        # df_dataset = convert_types(df_dataset, ds_config['dtypes'])
        # print(df_dataset)

        # print(f'Removendo linhas com dados obrigatórios que estão nulos...')
        # df_municipios = remove_null(df_municipios, municipios_config)

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