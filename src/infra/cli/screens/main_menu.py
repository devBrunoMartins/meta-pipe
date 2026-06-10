from utils.clear import clear
from infra.cli.input.entry_num import entry_num
from core.execution.execution import Execution
from core.execution.models.version import Version
from infra.cli.screens.version_details_menu import version_details_menu
from pipeline.prepare_new_pipeline import prepare_new_pipeline
from infra.cli.screens.version_delete import version_delete
from infra.cli.screens.version_resume import version_resume
from pipeline.run import pipeline_run
from infra.cli.screens.table_versions import table_versions


def menu_versions(versions: list[Version]):
    clear()
    print("""

====================================================================================
                                PIPELINES REGISTRADOS
====================================================================================
""")

    table_versions(versions)

    print(f"""

    [1] Criar execução
    [2] Continuar execução
    [3] Detalhar execução
    [4] Excluir execução
    [0] Encerrar sistema

====================================================================================
    """)


def empty_versions():
    print("""

====================================================================================
                            NÃO HÁ PIPELINES REGISTRADOS
====================================================================================

    [1] Criar execução
    [0] Encerrar sistema

====================================================================================
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

    option = entry_num('Digite a opção desejada: ', required=True)

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
