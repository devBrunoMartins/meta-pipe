from infra.cli.inputs import get_user_response_int
from core.execution.execution import Execution
from core.execution.models.version import Version

def version_resume(execution: Execution):

    versions = execution.find_pending_versions()
    if not versions:
        return 

    print("""

================================================================
                        VERSÕES PENDENTES
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

    print(f"""
====================================================================

    """)

    list_options = [version.id_version for version in versions]

    option = get_user_response_int(
"""Informe o ID da execução a ser deletada\n[0] Voltar\n
Digite a opção desejada: """)

    if option == 0:
        return None
    
    if option in list_options:
        version_selected = [version for version in versions
                            if version.id_version == option][0]

        return version_selected
        

    else:
        print('Opção inválida.')

    version_resume(execution)