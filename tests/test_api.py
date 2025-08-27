import unittest
import json

import yaml
from yaml import BaseLoader

from directus_sync.directus_sync import export
from directus_sync.config import Config


class TestIMAPSync(unittest.TestCase):
    def test_sync_all(self):
        with open("tests/prod.yml", "r") as f:
            dat = yaml.load(f, Loader=BaseLoader)
        config = Config.model_validate_json(json.dumps(dat))
        export(config)


if __name__ == "__main__":
    a = TestIMAPSync()

    a.test_sync_all()
