from typing import Iterator
import requests

from .models import Config, Contact


def read_contacts(config: Config) -> Iterator[Contact]:
    # https://directus.io/docs/getting-started/use-the-api
    res = requests.get(
        f"{config.directus_url}/Contacts",
        headers={"Authorization": f"Bearer {config.directus_token}"},
    )
    data = res.json()
    for c in data["data"]:
        contact = Contact.model_validate(c)
        yield contact
