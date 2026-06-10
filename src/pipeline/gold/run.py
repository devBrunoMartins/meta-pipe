from pipeline.gold.metrics.municipios_indicadores import build_gold_municipios_indicadores
from pipeline.gold.metrics.estados_resumo import build_gold_estados_resumo
from pipeline.gold.metrics.ranking_pib import build_gold_ranking_pib
from pipeline.gold.metrics.ranking_populacao import build_gold_ranking_populacao
from pipeline.gold.metrics.ranking_pib_per_capita import build_gold_ranking_pib_per_capita

from config.system.pipeline import DATA_DIR

from infra.io.load_parquet import load_parquet
from infra.paths.path_manager import prepare_path
from infra.io.save_parquet import save_parquet

from core.execution.execution import Execution



LAYER_NAME = 'gold'
LAYER_SILVER = 'silver'

def run(
        dataset_conf: list[dict],
        execution:Execution
    ) -> None:
    


    execution_metrics = {
        'gold_municipios_indicadores': build_gold_municipios_indicadores,
        'gold_estados_resumo': build_gold_estados_resumo,
        'gold_ranking_pib': build_gold_ranking_pib,
        'gold_ranking_populacao': build_gold_ranking_populacao,
        'gold_ranking_pib_per_capita': build_gold_ranking_pib_per_capita
    }

    
    layer = execution.get_layer_by_name(LAYER_NAME)
    pendings_assets = execution.pending_assets(layer)

    layer_silver = execution.get_layer_by_name(LAYER_SILVER)
    success_assets_silver = execution.success_assets(layer_silver)

    ############### ATENÇÃO DEV: Implementar código aqui ---
    ###### Caso haja alguma pendência em silver, não rodar gold ou apenas 
    ###### as métricas que não tem dependência faltante.

    print(f'Carregando todos os datasets...')
    path_dim_municipios = [asset.path for asset in success_assets_silver
                            if asset.name == 'municipios']
    dim_municipios = load_parquet(path=path_dim_municipios[0])


    path_fact_pib = [asset.path for asset in success_assets_silver
                     if asset.name == 'pib']
    fact_pib = load_parquet(path=path_fact_pib[0])
    

    path_fact_populacao = [asset.path for asset in success_assets_silver
                        if asset.name == 'populacao']
    fact_populacao = load_parquet(path=path_fact_populacao[0])

    datasets_availables = {
        'dim_municipios': dim_municipios,
        'fact_pib': fact_pib,
        'fact_populacao': fact_populacao
    }


    for metric_name, metric_function in execution_metrics.items():

        print(f'Gerando métrica: \033[36m{metric_name}\033[0m')

        columns = dataset_conf[metric_name]['columns']

        ds_list_config = [ds for ds, _ in columns.items()]
        using_datasets = {
            k: v
            for k, v in datasets_availables.items()
            if k in ds_list_config
        }

        order = dataset_conf[metric_name].get('order')
        if order:

            dataset = metric_function(
                datasets=using_datasets,
                columns=columns)[order]
        else: 
            dataset = metric_function(
                datasets=using_datasets,
                columns=columns)
            
        path = prepare_path(
            dataset = metric_name,
            data_dir = DATA_DIR,
            layer = LAYER_NAME,
            extension = 'parquet'
        )

        save_parquet(dataset=dataset, path=path)

        path = str(path)

        print(f'Salvo em: \033[36m{path}\033[0m\n')

        
        
        for asset in pendings_assets:
            if asset.name == metric_name:
                asset.path = path
                execution.asset_finish(asset)

    execution.layer_finish(layer)

# if __name__ == "__main__":
#     run()
