from typing import Any, Dict

import yaml
import os


class App:
    port: int
    name: str
    environment: str
    key: str
    migrate_key: str
    jwt_key: str

    def __init__(self, **data: Any):
        self.__dict__.update(**data)


class Database:
    host: str
    port: int
    name: str
    username: str
    password: str

    def __init__(self, **data: Any):
        self.__dict__.update(**data)


class Config:
    app: App
    database: Dict[str, Database]

    def __init__(self, data: Dict[str, Any]):
        self.app = App(**data["app"])
        self.database = dict((k, Database(**v)) for k, v in data["database"].items())


_config: Config | None = None


def load_config() -> None:
    global _config
    env = os.getenv("ENVIRONMENT", "develop")  # gak tau kenapa dari .env tidak terbaca
    path = os.path.dirname(os.path.abspath(__file__))
    with open(
        "{}/config-{}.yaml".format(path, env), "r"
    ) as stream:
        data = yaml.safe_load(stream)
        _config = Config(data)


def get_config() -> Config:
    global _config
    if _config is None:
        load_config()
        if _config is None:
            raise RuntimeError("Configuration could not be loaded")
    return _config
