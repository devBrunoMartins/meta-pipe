from core.io.save_json import save_json
from core.io.request_json import request_json
from core.paths.path_manager import prepare_path
from config.system.pipeline import DATA_DIR, HTTP_RETRIES, HTTP_TIMEOUT


LAYER = 'bronze'

def run(config: list[dict]):

    for dataset in config:

        print(
            f"Extraindo \033[36m{dataset['label']}\033[0m\n"
            f"URL: \033[36m{dataset['url']}\033[0m"
        )

        data_raw = request_json(
            url=dataset['url'],
            retries=HTTP_RETRIES,
            timeout=HTTP_TIMEOUT
        )

        path = prepare_path(
            dataset=dataset['name'],
            data_dir=DATA_DIR,
            layer=LAYER,
            extension='json'
        )

        save_json(data_raw, path)


if __name__=='__main__':
    ...