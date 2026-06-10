from infra.cli.input.entry import entry

def entry_alpha_num(message: str, required: bool = False) -> str | None:

    user_response = None

    while True:

        user_response = entry(message)

        if required and not user_response:
            print('\033[031mcampo obrigatório\033[0m')
            continue

        if user_response:
            if is_valid(user_response):
                return user_response
            else:
                print('\033[031mentrada inválida\033[0m')
                continue
        else:
            return None


def is_valid(user_response: None | str) -> bool:
    if user_response[0].isalpha():
        return True
    return False