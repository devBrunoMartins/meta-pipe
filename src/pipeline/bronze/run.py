from infra.io.save_json import save_json
from infra.io.request_json import request_json
from infra.paths.path_manager import prepare_path
from config.system.pipeline import DATA_DIR, HTTP_RETRIES, HTTP_TIMEOUT
from core.execution.execution import Execution

LAYER_NAME = 'bronze'


def run(
        dataset_conf: list[dict],
        execution: Execution
    ) -> None:
    
    
    layer = execution.get_layer_by_name(LAYER_NAME)
    pending_assets = execution.pending_assets(layer)


    for asset in pending_assets:

        conf = dataset_conf[asset.name]

        dataset_label = conf['label']
        dataset_name = asset.name
        dataset_url = conf['url']

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

        asset.path = str(path)
        print(f'Salvo em: \033[36m{str(path)}\033[0m\n')
        execution.asset_finish(asset)
      

    execution.layer_finish(layer)







if __name__=='__main__':
    ...