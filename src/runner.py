from pipeline.bronze.run import run as run_bronze
from src.pipeline.silver.run_silver import run as run_silver
from src.pipeline.gold.run_gold import run as run_gold

from config.datasets.municipios import MUNICIPIOS_CONFIG
from config.datasets.populacao import POPULACAO_CONFIG
from config.datasets.pib import PIB_CONFIG



def pipe_run():

    config = [
        PIB_CONFIG, 
        POPULACAO_CONFIG, 
        MUNICIPIOS_CONFIG
        ]


    # Executa camada bronze
    print(f"\n\033[33mExtract\033[0m")
    run_bronze(config=config)

    # Executa camada silver
    print(f"\n\033[33mTransform\033[0m")
    # run_silver()

    # Executa a camada Gold
    print(f"\n\033[33mMetrics\033[0m")
    # run_gold()
    
    print(f"\n\033[32mPronto!\033[0m\n")


if __name__ == '__main__':
    pipe_run()


    