from src.pipeline.bronze.run_bronze import run as run_bronze
from src.pipeline.silver.run_silver import run as run_silver
from src.pipeline.gold.run_gold import run as run_gold


def pipe_run():
    # Executa camada bronze
    print(f"\n\033[33mExtract\033[0m")
    run_bronze()

    # Executa camada silver
    print(f"\n\033[33mTransform\033[0m")
    run_silver()

    # Executa a camada Gold
    print(f"\n\033[33mMetrics\033[0m")
    run_gold()
    
    print(f"\n\033[32mPronto!\033[0m\n")


if __name__ == '__main__':
    pipe_run()