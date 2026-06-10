from infra.cli.input.entry_num import entry_num
from core.execution.execution import Execution
from infra.cli.screens.version_details import version_details
from utils.clear import clear
from infra.cli.screens.table_versions import table_versions


def version_details_menu(execution: Execution):
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

    print(f"""
====================================================================================

    """)

    list_options = [version.id_version for version in versions]

    option = entry_num('Informe o ID da execução desejada ou [0] para retornar: ', required=True)

    if option == 0:
        return 'show_main_menu'
    
    if option in list_options:
        version_selected = [version for version in versions
                            if version.id_version == option][0]
        version_details(execution, version_selected)

    else:
        print('Opção inválida.')

    version_details_menu(execution)