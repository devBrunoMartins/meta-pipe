import sqlite3
from pathlib import Path

from pipeline.bronze.run import run as run_bronze
from src.pipeline.silver.run import run as run_silver
# from src.pipeline.gold.run import run as run_gold

from config.system.pipeline import METADATA_DIR, METADATA_NAME

from config.datasets.municipios import MUNICIPIOS_CONFIG
from config.datasets.populacao import POPULACAO_CONFIG
from config.datasets.pib import PIB_CONFIG

from infra.db.sqlite_db import SQLiteDB
from infra.db.repository import RepositoryPipeline
from core.execution.versioning import Versioning
from infra.paths.path_manager import ensure_path

config = [
    PIB_CONFIG, 
    POPULACAO_CONFIG, 
    MUNICIPIOS_CONFIG
    ]


def pipe_run():

    #################################################################
    ### START
    #################################################################

    path_db = METADATA_DIR / METADATA_NAME
    ensure_path(METADATA_DIR)

    conn = sqlite3.connect(path_db)
    db = SQLiteDB(conn)
    repo = RepositoryPipeline(db)
    versioning = Versioning(repo)

    versioning.run()


    #################################################################
    ### LAYER BRONZE
    #################################################################
    
    print(f"\n\033[33mExtract\033[0m")

    run_bronze(config, versioning)
    

    #################################################################
    ### LAYER SILVER
    #################################################################
    
    # print(f"\n\033[33mTransform\033[0m")

    # run_silver(config=config)


    #################################################################
    ### LAYER GOLD
    #################################################################
    # print(f"\n\033[33mMetrics\033[0m")
    # run_gold()
    

    #################################################################
    ########################### THE END #############################
    #################################################################
    
    print(f"\n\033[32mPronto!\033[0m\n")


if __name__ == '__main__':
    pipe_run()
    

    