import sqlite3

from pipeline.bronze.run import run as run_bronze
from src.pipeline.silver.run import run as run_silver
# from src.pipeline.gold.run import run as run_gold

from config.system.pipeline import METADATA_DIR, METADATA_NAME

from config.datasets.municipios import MUNICIPIOS_CONFIG
from config.datasets.populacao import POPULACAO_CONFIG
from config.datasets.pib import PIB_CONFIG


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
    conn = sqlite3.connect(path_db)
    db = SQLiteDB(conn)
    repo = Repository(db)
    versioning = Versioning(repo)

    #################################################################
    ### LAYER BRONZE
    #################################################################
    
    print(f"\n\033[33mExtract\033[0m")

    run_bronze(config=config)
    

    #################################################################
    ### LAYER SILVER
    #################################################################
    
    print(f"\n\033[33mTransform\033[0m")

    run_silver(config=config)


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
    

    