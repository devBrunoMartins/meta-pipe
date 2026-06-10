from core.execution.models.version import Version


def table_versions(versions: list[Version]) -> None:
    for version in versions:
        if version.status == 'success':
            status_color = '\033[032m'
        else:
            status_color = '\033[031m'

        finished_at = version.finished_at or '---'
        description = version.description or '---'
        print(
            f"ID: \033[036m{version.id_version:<3}\033[0m "
            f"Nome: \033[035m{version.name:<20}\033[0m "
            f"Descrição: \033[035m{description:<20}\033[0m "
            f"Status: {status_color}{version.status:<9}\033[0m"
            f"Início: \033[036m{version.start_at:<20}\033[0m "
            f"Fim: \033[036m{finished_at:<20}\033[0m"
            )