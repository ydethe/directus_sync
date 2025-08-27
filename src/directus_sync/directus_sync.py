import requests

from .config import Config


def export(config: Config):
    # https://directus.io/docs/getting-started/use-the-api
    res = requests.get(
        f"{config.directus_url}/Contacts",
        headers={"Authorization": f"Bearer {config.directus_token}"},
    )
    print(res.json())
