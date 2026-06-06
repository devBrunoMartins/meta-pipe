import sqlite3
from pathlib import Path

from pipeline.bronze.run import run as run_bronze
from src.pipeline.silver.run import run as run_silver
from src.pipeline.gold.run import run as run_gold

from config.system.pipeline import METADATA_DIR, METADATA_NAME

from config.pipeline.bronze import BRONZE_DATASET_CONFIG
from config.pipeline.silver import SILVER_DATASET_CONFIG
from config.pipeline.gold import GOLD_DATASET_CONFIG

from infra.db.sqlite_db import SQLiteDB
from core.execution.execution import Execution
from infra.repositories.version_repository import VersionRepository
from infra.repositories.layer_repository import  LayerRepository
from infra.repositories.asset_repository import AssetRepository

from core.execution.models.version import Version
from core.execution.models.layer import Layer
from core.execution.models.asset import Asset


from core.execution.execution import Execution
from infra.paths.path_manager import ensure_path

from infra.cli import inputs
from infra.cli import menu

from datetime import datetime
from zoneinfo import ZoneInfo


def pipe_run():

    #################################################################
    ### START
    #################################################################

    path_db = METADATA_DIR / METADATA_NAME
    ensure_path(METADATA_DIR)

    conn = sqlite3.connect(path_db)
    db = SQLiteDB(conn)
    version_repository = VersionRepository(db)
    layer_repository = LayerRepository(db)
    asset_repository = AssetRepository(db)

    execution = Execution(
        version_repository = version_repository,
        layer_repository = layer_repository,
        asset_repository = asset_repository        
    )

    execution.init_db()

    pending_versions = execution.find_pending_versions()

    if pending_versions:
        menu.show_pending_menu(pending_versions)
        response = inputs.get_user_response_int('Digite a opção desajada: ')
        # Continuar depois

    else:
        menu.show_main_menu()
        response = inputs.get_user_response_int('Digite a opção desajada: ')

        if response == 1:
            menu.show_info_pipeline_menu()

            name = inputs.get_user_response_str('Nome..............: ')
            description = inputs.get_user_response_str('Descrição.........: ')

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


    #################################################################
    ### LAYER BRONZE
    #################################################################
    print(f"\n\033[35mIniciando Extração\033[0m")
    run_bronze(BRONZE_DATASET_CONFIG, execution)


    #################################################################
    ### LAYER SILVER
    #################################################################
    print(f"\n\033[35mIniciando Transformação\033[0m")
    run_silver(SILVER_DATASET_CONFIG, execution)


    #################################################################
    ### LAYER GOLD
    #################################################################
    print(f"\n\033[35mIniciando Cálculos de Métricas\033[0m")
    run_gold(GOLD_DATASET_CONFIG, execution)
    

    #################################################################
    ########################### THE END #############################
    #################################################################
    
    finished_at = datetime.now(
        ZoneInfo("America/Sao_Paulo")
        ).strftime("%Y-%m-%d %H:%M:%S")
    
    execution.finish(
        finished_at = finished_at,
        status = 'success'
    )
    
    print(f"\n\033[32mPronto!\033[0m\n")


if __name__ == '__main__':
    pipe_run()
    

    