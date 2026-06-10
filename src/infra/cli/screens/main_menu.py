from infra.cli.inputs import get_user_response_int
from core.execution.execution import Execution
from core.execution.models.version import Version
from infra.cli.screens.version_details_menu import version_details_menu
from pipeline.prepare_new_pipeline import prepare_new_pipeline
from infra.cli.screens.version_delete import version_delete
from infra.cli.screens.version_resume import version_resume
from pipeline.run import pipeline_run
import sys


def menu_versions(versions: list[Version]):
    print("""

================================================================
                    PIPELINES REGISTRADOS
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

    [1] Criar execução
    [2] Continuar execução
    [3] Detalhar execução
    [4] Excluir execução
    [0] Encerrar sistema

================================================================
    """)


def empty_versions():
    print("""

================================================================
                NÃO HÁ PIPELINES REGISTRADOS
================================================================

    [1] Criar execução
    [0] Encerrar sistema

================================================================
        """)




def main_menu(execution: Execution) -> None:
    
    versions = execution.get_versions()
    limit_options = None

    if versions:
        menu_versions(versions)
        limit_options = 4
    else:
        empty_versions()
        limit_options = 1

    option = get_user_response_int('Digite a opção desejada: ')

    if 0 <= option <= limit_options:

        if option == 0:
            return

        elif option == 1:
            prepare_new_pipeline(execution)
            pipeline_run(execution)

        elif option == 2:
            version_selected = version_resume(execution)

            if version_selected:
                execution.load_version_pending(version=version_selected)
                pipeline_run(execution)

        elif option == 3:
            version_details_menu(execution)

        elif option == 4:
            version_delete(execution)
    else:
        print('Opção inválida.')

    main_menu(execution)
