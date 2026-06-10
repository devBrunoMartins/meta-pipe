from infra.cli.input.entry_num import entry_num
from core.execution.execution import Execution
from utils.clear import clear
from infra.cli.screens.table_versions import table_versions

def version_resume(execution: Execution):
    clear()
    
    versions = execution.find_pending_versions()
    if not versions:
        return 

    print("""

====================================================================================
                                  VERSÕES PENDENTES
====================================================================================
""")

    table_versions(versions)

    print(f"""
====================================================================================

    """)

    list_options = [version.id_version for version in versions]

    option = entry_num(
"""Informe o ID da execução a ser deletada\n[0] Voltar\n
Digite a opção desejada: """, required=True)

    if option == 0:
        return None
    
    if option in list_options:
        version_selected = [version for version in versions
                            if version.id_version == option][0]

        return version_selected
        

    else:
        print('Opção inválida.')

    version_resume(execution)