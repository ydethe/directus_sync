from typing import Any, Iterator
import requests

from .models import Config, Contact, Adresse


def request_collection(config: Config, collection: str) -> dict[Any, Any]:
    # https://directus.io/docs/getting-started/use-the-api
    res = requests.get(
        f"{config.directus_url}/{collection}",
        headers={"Authorization": f"Bearer {config.directus_token}"},
    )
    data = res.json()

    return data["data"]


def read_contacts(config: Config) -> Iterator[Contact]:
    data = request_collection(config, collection="Contacts")
    for c in data:
        contact = Contact.model_validate(c)
        yield contact


def read_adresses(config: Config) -> Iterator[Adresse]:
    data = request_collection(config, collection="Adresse")
    for a in data:
        adresse = Adresse.model_validate(a)
        yield adresse
