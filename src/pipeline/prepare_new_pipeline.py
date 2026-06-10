from config.pipeline.bronze import BRONZE_DATASET_CONFIG
from config.pipeline.silver import SILVER_DATASET_CONFIG
from config.pipeline.gold import GOLD_DATASET_CONFIG

from core.execution.execution import Execution

from infra.cli.inputs import get_user_response_str


def prepare_new_pipeline(execution: Execution):

    name = get_user_response_str('Nome..............: ')
    description = get_user_response_str('Descrição.........: ')

    execution.init_version(
        name=name,
        description=description,
    )

    ### Loads the Bronze layer's assets
    print(f'Lendo arquivos de configuração dos datasets...')
    id_layer_bronze = execution.init_layer(
        name='bronze'
    )
    for name, _ in BRONZE_DATASET_CONFIG.items():
        execution.init_assets(
            id_layer = id_layer_bronze,
            name = name
        )

    ### Loads the Silver layer's assets
    id_layer_silver = execution.init_layer(
        name='silver'
    )
    for name, _ in SILVER_DATASET_CONFIG.items():
        execution.init_assets(
            id_layer = id_layer_silver,
            name = name
        )


    ### Loads the Gold layer's assets
    id_layer_gold = execution.init_layer(
        name='gold'
    )
    for name, _ in GOLD_DATASET_CONFIG.items():
        execution.init_assets(
            id_layer = id_layer_gold,
            name = name
        )
