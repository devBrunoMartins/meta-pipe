from infra.paths.path_manager import remove_files
from core.execution.execution import Execution
from infra.cli.inputs import get_user_response_int
from pathlib import Path


def version_delete(execution: Execution):

    versions = execution.get_versions()
    if not versions:
        return 

    
    print("""

================================================================
                        VERSÕES REGISTRADAS
================================================================
""")

    for version in versions:
        if version.status == 'success':
            status_color = '\033[032m'
        else:
            status_color = '\033[031m'

        finished_at = version.finished_at or '---'

        print(
            f"ID: \033[036m{version.id_version:<3}\033[0m "
            f"Nome: \033[035m{version.name:<20}\033[0m "
            f"Descrição: \033[035m{version.description:<20}\033[0m "
            f"Status: {status_color}{version.status:<9}\033[0m"
            f"Início: \033[036m{version.start_at:<20}\033[0m "
            f"Fim: \033[036m{finished_at:<20}\033[0m"
            )
    print("""
--------------------------------------------------------------------

        Selecione uma execução para excluir.
        \033[031m Atenção: todos os registros serão excluídos! \033[0m

====================================================================

    """)


    list_options = [version.id_version for version in versions]

    option = get_user_response_int(
"""Informe o ID da execução a ser deletada\n[0] Voltar\n
Digite a opção desejada: """)
    
    if option == 0:
        return
    
    if option in list_options:

        version = [version for version in execution.get_versions()
                   if version.id_version == option][0]
        
        assets = [Path(asset.path) for asset in execution.get_assets_by_version(version) if asset.path]

        remove_files(assets)
        execution.delete_version(option)
        
    else:
        print('Opção inválida.')

    version_delete(execution)
