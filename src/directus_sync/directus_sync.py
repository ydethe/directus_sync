import requests

from .config import Config


def export(config: Config):
    res = requests.get(
        str(config.directus_url), headers={"Authorization": f"Bearer {config.directus_token}"}
    )
    print(res.json())
