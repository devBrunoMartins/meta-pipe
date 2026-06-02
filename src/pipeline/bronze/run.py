from core.io.save_json import save_json
from core.io.request_json import request_json
from core.paths.path_manager import prepare_path
from config.system.pipeline import DATA_DIR, HTTP_RETRIES, HTTP_TIMEOUT
from core.execution.versioning import Versioning

LAYER_NAME = 'bronze'

def run(config: list[dict], versioning:Versioning) -> None:

    for dataset in config:

        dataset_name = dataset['name']
        dataset_label = dataset['label']
        dataset_url = dataset['url']

        print(
            f"Extraindo \033[36m{dataset_label}\033[0m\n"
            f"URL: \033[36m{dataset_url}\033[0m"
        )

        data_raw = request_json(
            url=dataset_url,
            retries=HTTP_RETRIES,
            timeout=HTTP_TIMEOUT
        )

        path = prepare_path(
            dataset=dataset_name,
            data_dir=DATA_DIR,
            layer=LAYER_NAME,
            extension='json'
        )

        save_json(data_raw, path)

        versioning.registry_asset(
            layer_name=LAYER_NAME,
            name=dataset_name,
            path=str(path)
            )


if __name__=='__main__':
    ...