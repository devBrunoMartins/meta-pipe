from infra.cli.screens.goodbye import goodbye


def entry(message: str) -> int:
    try:
        return input(message)

    except (EOFError, KeyboardInterrupt) as erreof:
        goodbye()

    except Exception as err:
        raise err

        




if __name__ == '__main__':
    ...