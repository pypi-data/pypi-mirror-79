from deoxys.model import Model, model_from_full_config
from deoxys.utils import read_file


def test_load():
    pass


def test_save():
    pass


def test_from_config():
    config = read_file('tests/json/sequential-config.json')
    model_from_full_config(config)
