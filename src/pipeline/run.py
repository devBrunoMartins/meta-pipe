from pipeline.bronze.run import run as run_bronze
from src.pipeline.silver.run import run as run_silver
from src.pipeline.gold.run import run as run_gold

from config.pipeline.bronze import BRONZE_DATASET_CONFIG
from config.pipeline.silver import SILVER_DATASET_CONFIG
from config.pipeline.gold import GOLD_DATASET_CONFIG

from core.execution.execution import Execution


def pipeline_run(execution: Execution):

    #################################################################
    ### LAYER BRONZE
    #################################################################
    print(f"\n\033[35mIniciando Extração\033[0m")
    run_bronze(BRONZE_DATASET_CONFIG, execution)


    #################################################################
    ### LAYER SILVERexecution.load_version_pending(version=version_selected)
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
    

    
    execution.finish()
    
    print(f"\033[32mSucesso!\033[0m\n\n")


if __name__ == '__main__':
    pipeline_run()
    

    