def show_pending_menu(pending_versions: list) -> None:

    print("""\n
    ============================================================
                    EXECUÇÕES PENDENTES ENCONTRADAS
    ============================================================
    """)

    for version in pending_versions:
        print(
            f"[ID: {version.id_version}] "
            f"{version.name} | "
            f"start_at: {version.start_at}"
        )

    print("""
    ------------------------------------------------------------

    [1] Continuar uma execução pendente
    [2] Cancelar uma execução pendente
    [3] Excluir uma execução pendente e todos os seus registros
    [4] Iniciar uma nova execução
    [0] Voltar ao menu principal
    ============================================================
    """)


def show_main_menu() -> None:
    print("""
    ============================================================
                        DATA PIPELINE
    ============================================================

    Status: Nenhuma execução pendente.

    [1] Iniciar nova execução
    [2] Listar versões
    [3] Consultar versão
    [4] Excluir versão
    [0] Encerrar aplicação

    ============================================================
    """)


def show_info_pipeline_menu() -> None:
    print("""
    ============================================================
                    NOVA EXECUÇÃO DE PIPELINE
    ============================================================

    Informe os dados da nova execução.

    ============================================================
    """)
