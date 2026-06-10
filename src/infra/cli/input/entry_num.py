from infra.cli.input.entry import entry

def entry_num(message: str, required: bool = False) -> int | None:

    user_response = None

    while True:

        user_response = entry(message)

        if required and not user_response:
            print('\033[031mcampo obrigatório\033[0m')
            continue

        if user_response:
            if is_valid(user_response):
                return int(user_response)
            else:
                print('\033[031mentrada inválida\033[0m')
                continue
        else:
            return user_response

def is_valid(user_response: None | str) -> bool:

    if user_response.isdigit():
        return True
    return False