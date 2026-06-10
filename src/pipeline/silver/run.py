from config.system.pipeline import DATA_DIR
from pipeline.silver.transform.dataframe import to_dataframe
from infra.io.load_json import load_json
from pipeline.silver.transform.convert_dtypes import convert_types
from pipeline.silver.transform.rename import columns_rename
from pipeline.silver.transform.remove_nulls import remove_nulls
from pipeline.silver.transform.delete_duplicates import delete_duplicates
from infra.paths.path_manager import prepare_path
from infra.io.save_parquet import save_parquet
from core.execution.execution import Execution


LAYER_NAME = 'silver'
LAYER_BRONZE = 'bronze'

def run(
        dataset_conf: list[dict],
        execution:Execution
    ) -> None:

    layer_bronze = execution.get_layer_by_name(LAYER_BRONZE)
    success_assets_bronze = execution.success_assets(layer_bronze)


    layer = execution.get_layer_by_name(LAYER_NAME)
    pending_assets = execution.pending_assets(layer)


    for asset_silver in pending_assets:

        ds_config = dataset_conf[asset_silver.name]
        name = asset_silver.name
        prefix = ds_config['table_prefix']
        columns = ds_config['columns']
        columns_not_null = ds_config['constraints']['not_null']
        columns_unique =  ds_config['constraints']['unique']
        dtypes = ds_config['dtypes']

        path_bronze = [asset.path for asset in success_assets_bronze
                       if asset.name == asset_silver.name][0]

        print(f'Carregando dados brutos do dataset \033[36m{ds_config['label']}\033[0m \nsource: \033[36m{path_bronze}\033[0m')
        json_dataset = load_json(path_bronze)
        
        print(f'Gerando DataFrame...')
        df_dataset = to_dataframe(json_dataset, ds_config)

        print(f'Renomeando colunas...')
        df_dataset = columns_rename(df_dataset, columns)

        print(f'Convertendo os tipos de dados...')
        df_dataset = convert_types(df_dataset, dtypes)

        print(f'Removendo linhas com dados obrigatórios que estão nulos...')
        df_dataset = remove_nulls(df_dataset, columns_not_null)

        print(f'Removendo linhas duplicadas...')
        df_dataset = delete_duplicates(df_dataset, columns_unique)
        
        dataset_name = (f"{prefix}_{name}")
        
        path = prepare_path(
        dataset=dataset_name,
        data_dir=DATA_DIR,
        layer=LAYER_NAME,
        extension='parquet'
        )

        save_parquet(df_dataset, path)

        asset_silver.path = str(path)
        print(f'Salvo em: \033[36m{str(path)}\033[0m\n')


        execution.asset_finish(asset_silver)
       

    execution.layer_finish(layer)



if __name__=='__main__':
    ...