from infra.cli.inputs import get_user_response_int
from infra.cli.screens.version_details_menu import version_details_menu
from infra.cli.screens.version_delete import version_delete
from core.execution.execution import Execution
from core.execution.models.version import Version

def show_versions(versions: Version):
    for version in versions:
        print(
            f"ID: \033[036m{version.id_version}\033[0m | "
            f"Nome: \033[035m{version.name}\033[0m | "
            f"Descrição: \033[035m{version.description}\033[0m | "
            f"Status: \033[033m{version.status}\033[0m | "
            f"Início: \033[036m{version.start_at}\033[0m | "
            f"Fim: \033[036m{version.finished_at}\033[0m"
        )

def show_menu():
    print("""

----------------------------------------------------------------

    [1] Consultar detalhes
    [2] Excluir execução

      """)


def version_manager_menu(execution: Execution):

    versions = execution.get_versions()

    print("""\n
================================================================
                     GERENCIAR EXECUÇÕES
================================================================
    """)

    if versions:
        show_versions(versions)
        show_menu()
    else:
        print("""
    \033[032m Não há versões registradas\033[0m """)
  
    print("""    
    [0] Voltar ao menu principal
    
================================================================
    """)

    option = get_user_response_int('Digite a opção desejada: ')
    if option == 0:
        return
    
    elif versions and option == 1:
        version_details_menu(execution)

    elif versions and option == 2:
        version_delete(execution)
        

    else:
        print('Opção inválida.')

    version_manager_menu(execution)
