import typing
from configparser import ConfigParser
from pathlib import Path

COMPANIES_JSON_PATH = Path(__file__).parent.joinpath("data", "companies.json")
DATABASE_INI_PATH = Path(__file__).parent.joinpath("database.ini")


def config(filename: typing.Any = DATABASE_INI_PATH, section: str = "postgresql") -> dict:
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db
