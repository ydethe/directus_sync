import unittest
import json

import yaml
from yaml import BaseLoader

from directus_sync.directus_backend import read_contacts
from directus_sync.directus_sync import export
from directus_sync.models import Config
from directus_sync.vcard import Name, VCard


class TestDirectusSync(unittest.TestCase):
    def test_vcard(self):
        with open("tests/prod.yml", "r") as f:
            dat = yaml.load(f, Loader=BaseLoader)
        config = Config.model_validate_json(json.dumps(dat))
        for contact in read_contacts(config):
            vcard = VCard(
                fn=f"{contact.Prenom}{contact.Particule}{contact.Nom}",
                n=Name(
                    family=f"{contact.Particule}{contact.Nom}".strip(),
                    given=contact.Prenom,
                    prefixes=[contact.Civilite],
                ),
                anniversary=contact.Date_de_naissance,
                # gender: Optional[Gender] = None
                # adr: Optional[List[Address]] = None
                # tel: Optional[List[Telephone]] = None
                # email: Optional[List[Email]] = None
                title=contact.Civilite,
                # role: Optional[str] = None
                # org: Optional[Organization] = None
            )
            dscard = vcard.to_vcard()
            print(dscard)

    def test_sync_all(self):
        with open("tests/prod.yml", "r") as f:
            dat = yaml.load(f, Loader=BaseLoader)
        config = Config.model_validate_json(json.dumps(dat))
        export(config)


if __name__ == "__main__":
    a = TestDirectusSync()

    a.test_vcard()
    # a.test_sync_all()
