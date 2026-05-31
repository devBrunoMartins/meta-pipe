import requests


def request_json(
        url: str,
        retries: int,
        timeout: int,
        params: dict | None = None):
    
    # Request data form the API
    for attempt in range(1, retries + 1):
        
        try:

            response = requests.get(url=url, params=params, timeout=timeout)

            response.raise_for_status()

            data = response.json()

            return data
        
        except requests.HTTPError as errh:
            print(f'Erro de HTTP: {errh}')

        except requests.ConnectionError as errc:
            print(f'Erro de conexão: {errc}')

        except requests.Timeout as errt:
            print(f'Erro. Tempo limite atingido. {errt}')

        except requests.RequestException as erre:
            print(f'Erro inesperado: {erre}')

        print(f'\nTentativa {attempt}/{retries} falhou.\n')

        if attempt == retries:
            raise

    

if __name__=='__main__':
    ...