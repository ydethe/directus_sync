from .models import Config
from .directus_backend import (
    read_contacts,
    read_adresses,
    read_contact_adresses,
    read_experience,
    read_organisation,
    read_organisation_adresses,
    read_telephone,
)


def export(config: Config):
    for contact in read_contacts(config):
        print(contact)

    for adresse in read_adresses(config):
        print(adresse)

    for con_adr in read_contact_adresses(config):
        print(con_adr)

    for expe in read_experience(config):
        print(expe)

    for orga in read_organisation(config):
        print(orga)

    for orga_adr in read_organisation_adresses(config):
        print(orga_adr)

    for tel in read_telephone(config):
        print(tel)
