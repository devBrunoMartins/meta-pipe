
def get_user_response_int(message: str) -> int:
    while True:
        option = input(message).strip()
        if option.isalnum() and 0 <= int(option) <= 4:
            return int(option)
        print('Opção inválida!\n')



def get_user_response_str(message: str) -> int:
    while True:
        option = input(message).strip()
        if option and option[:1].isalpha():
            return option
        print('Opção inválida!\n')

