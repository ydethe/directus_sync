import requests

from .config import Config


def export(config: Config):
    # https://directus.io/docs/getting-started/use-the-api#fetching-data
    res = requests.get(
        str(config.directus_url), headers={"Authorization": f"Bearer {config.directus_token}"}
    )
    print(res.json())
