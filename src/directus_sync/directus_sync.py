from .models import Config
from .directus_backend import read_contacts


def export(config: Config):
    for contact in read_contacts(config):
        print(contact)
