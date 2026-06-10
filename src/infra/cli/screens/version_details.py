from infra.cli.input.entry_num import entry_num
from core.execution.execution import Execution
from core.execution.models.version import Version
from utils.clear import clear

def version_details(execution: Execution, version: Version):
    clear()
    
    status_color = {
        "success": "\033[32m",
        "pending": "\033[33m",
        "failed": "\033[31m",
    }
    reset = "\033[0m"

    print(f"""

====================================================================================
                                DETALHES DA EXECUÇÃO
====================================================================================

ID...............: {version.id_version}
Nome.............: {version.name}
Descrição........: {version.description}
Status...........: {version.status}
Início...........: {version.start_at}
Fim..............: {version.finished_at}

====================================================================================
                                       CAMADAS
====================================================================================
""")
    layers = execution.get_layers_by_version(version)

    for layer in layers:
        print(f"""
Camada: {layer.name.upper()}
Status: {layer.status}
ID: {layer.id_layer}

        Assets:
""")
        assets = execution.get_assets_by_layer(layer)
        if not assets:
            print("        (nenhum asset encontrado)")
            continue

        for asset in assets:
            print(
                f"        - {asset.name:<35} | "
                f"Status: {status_color.get(asset.status, '')}"
                f"{asset.status}{reset}"
            )
        print("""
--------------------------------------------------------------------------------""")
    print("""

    [0] Voltar
          
====================================================================================
""")
    while True:
        option = entry_num('Digite a opção desejada: ', required=True)
        if option == 0:
            return
        print('Opção inválida.')