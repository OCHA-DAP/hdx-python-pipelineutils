"""Global fixtures"""

from pathlib import Path

import pytest
from hdx.api.configuration import Configuration
from hdx.api.locations import Locations
from hdx.location.country import Country
from hdx.utilities.dateparse import parse_date

from hdx.python.pipelineutils import string_params_to_dict
from hdx.python.pipelineutils.reader import Read


@pytest.fixture(scope="session")
def fixtures():
    return Path("tests") / "fixtures"


@pytest.fixture(scope="session")
def input_folder(fixtures):
    return fixtures / "input"


@pytest.fixture(scope="session")
def configuration(fixtures, input_folder):
    Configuration._create(
        hdx_read_only=True,
        hdx_site="prod",
        user_agent="test",
        project_config_yaml=Path("tests") / "config" / "project_configuration.yaml",
    )
    Locations.set_validlocations(
        [
            {"name": "afg", "title": "Afghanistan"},
            {"name": "phl", "title": "Philippines"},
            {"name": "pse", "title": "State of Palestine"},
        ]
    )
    Country.countriesdata(use_live=False)

    header_auths = "population:pop_12345,who_national:who_abc"
    basic_auths = (
        "access:YWNjXzEyMzQ1OmFjY19hYmM=,who_national2:d2hvX2RlZjp3aG9fMTIzNDU="
    )
    bearer_tokens = "fts:12345"
    param_auths = "sadd:user=sadd_123&pass=sadd_abc,ourworldindata:auth=owid_abc"

    header_auths = string_params_to_dict(header_auths)
    basic_auths = string_params_to_dict(basic_auths)
    param_auths = string_params_to_dict(param_auths)
    today = parse_date("2020-10-01")
    save = False
    if save:
        Read.create_readers(
            "",
            fixtures / "tmp",
            "",
            save=True,
            use_saved=False,
            user_agent="test",
            header_auths=header_auths,
            basic_auths=basic_auths,
            bearer_tokens=bearer_tokens,
            param_auths=param_auths,
            today=today,
        )
    else:
        Read.create_readers(
            "",
            input_folder,
            "",
            save=False,
            use_saved=True,
            user_agent="test",
            header_auths=header_auths,
            basic_auths=basic_auths,
            param_auths=param_auths,
            today=today,
        )

    return Configuration.read()
