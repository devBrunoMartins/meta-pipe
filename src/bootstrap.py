import sqlite3

from infra.repositories.version_repository import VersionRepository
from infra.repositories.layer_repository import  LayerRepository
from infra.repositories.asset_repository import AssetRepository
from config.system.pipeline import METADATA_DIR, METADATA_NAME
from infra.paths.path_manager import ensure_path
from core.execution.execution import Execution
from infra.db.sqlite_db import SQLiteDB
from utils.clear import clear

def bootstrap():
    clear()
    
    #################################################################
    ############################ START ##############################
    #################################################################

    path_db = METADATA_DIR / METADATA_NAME
    ensure_path(METADATA_DIR)

    conn = sqlite3.connect(path_db)
    db = SQLiteDB(conn)
    conn.execute("PRAGMA foreign_keys = ON")

    version_repository = VersionRepository(db)
    layer_repository = LayerRepository(db)
    asset_repository = AssetRepository(db)

    execution = Execution(
        version_repository = version_repository,
        layer_repository = layer_repository,
        asset_repository = asset_repository        
    )

    execution.init_db()

    return execution