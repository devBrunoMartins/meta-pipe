from pathlib import Path

from infra.paths.path_manager import remove_files
from core.execution.execution import Execution
from infra.cli.input.entry_num import entry_num
from utils.clear import clear
from infra.cli.screens.table_versions import table_versions

def version_delete(execution: Execution):
    clear()
    
    versions = execution.get_versions()
    if not versions:
        return 

    
    print("""

====================================================================================
                                VERSÕES REGISTRADAS
====================================================================================
""")

    table_versions(versions)
    print("""
------------------------------------------------------------------------------------

        Selecione uma execução para excluir.
        \033[031m Atenção: todos os registros serão excluídos! \033[0m

====================================================================================

    """)


    list_options = [version.id_version for version in versions]

    option = entry_num(
"""Informe o ID da execução a ser deletada\n[0] Voltar\n
Digite a opção desejada: """, required=True)
    
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
