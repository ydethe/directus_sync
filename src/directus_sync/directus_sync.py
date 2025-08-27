from .models import Config
from .directus_backend import read_contacts, read_adresses


def export(config: Config):
    for contact in read_contacts(config):
        print(contact)

    for adresse in read_adresses(config):
        print(adresse)
