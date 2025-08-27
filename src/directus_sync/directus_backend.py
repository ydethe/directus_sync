from typing import Any, Callable, Dict, Iterator, List, TypeVar
import requests

from .models import (
    Config,
    Contact,
    Adresse,
    ContactsAdresse,
    Experience,
    Organisation,
    OrganisationsAdresse,
    Telephone,
)


T = TypeVar("T")


def request_collection(config: Config, collection: str) -> List[Dict[Any, Any]]:
    # https://directus.io/docs/getting-started/use-the-api
    res = requests.get(
        f"{config.directus_url}/{collection}",
        headers={"Authorization": f"Bearer {config.directus_token}"},
    )
    data = res.json()

    return data["data"]


def read_item(
    config: Config, collection: str, model_factory: Callable[[Dict[Any, Any]], T]
) -> Iterator[T]:
    data = request_collection(config, collection=collection)
    for dat in data:
        item = model_factory(dat)
        yield item


def read_contacts(config: Config) -> Iterator[Contact]:
    for contact in read_item(config, collection="Contacts", model_factory=Contact.model_validate):
        yield contact


def read_adresses(config: Config) -> Iterator[Adresse]:
    for adresse in read_item(config, collection="Adresse", model_factory=Adresse.model_validate):
        yield adresse


def read_contact_adresses(config: Config) -> Iterator[ContactsAdresse]:
    for con_adr in read_item(
        config, collection="Contacts_Adresse", model_factory=ContactsAdresse.model_validate
    ):
        yield con_adr


def read_experience(config: Config) -> Iterator[Experience]:
    for expe in read_item(config, collection="Experience", model_factory=Experience.model_validate):
        yield expe


def read_organisation(config: Config) -> Iterator[Organisation]:
    for expe in read_item(
        config, collection="Organisation", model_factory=Organisation.model_validate
    ):
        yield expe


def read_organisation_adresses(config: Config) -> Iterator[OrganisationsAdresse]:
    for orga_adr in read_item(
        config, collection="Organisation_Adresse", model_factory=OrganisationsAdresse.model_validate
    ):
        yield orga_adr


def read_telephone(config: Config) -> Iterator[Telephone]:
    for telephone in read_item(
        config, collection="Telephone", model_factory=Telephone.model_validate
    ):
        yield telephone
