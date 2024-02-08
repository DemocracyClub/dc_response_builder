import importlib

import pytest
from uk_election_ids.datapackage import ELECTION_TYPES, VOTING_SYSTEMS

from build.lib.response_builder.v1.sandbox import SANDBOX_POSTCODES
from response_builder.v1.builders.ballots import StockLocalBallotBuilder
from response_builder.v1.builders.base import RootBuilder, AbstractBuilder
from response_builder.v1.generated_responses.root_responses import (
    POLLING_STATION,
)
from response_builder.v1.models.base import RootModel


def test_building_sets_builder():
    builder = RootBuilder()
    assert isinstance(builder, RootBuilder)
    built = builder.build()
    assert isinstance(built, RootModel)


def test_root_builder():
    builder = RootBuilder()
    assert builder.build().dict() == {
        "address_picker": False,
        "addresses": [],
        "dates": [],
        "electoral_services": None,
        "registration": None,
    }


def test_address_picker_cant_have_ballots():
    """
    When we show an address picker, we don't show any ballots.

    We enforce this in the builder.
    """

    # Build a model with a ballot and no address picker
    builder = RootBuilder()
    ballot = StockLocalBallotBuilder()
    builder.with_ballot(ballot.build())
    builder.with_polling_station(POLLING_STATION)
    built = builder.build()
    assert not built.address_picker
    assert built.dates
    assert built.dates[0].polling_station.polling_station_known

    # Now add an address picker
    builder.with_address_picker()
    built = builder.build()
    assert built.address_picker
    assert not built.dates


def generate_expected_data():
    # Ballots
    all_data = [
        ("polling_stations", "WITH_MAP_POLLING_STATION"),
        ("polling_stations", "WITHOUT_MAP_POLLING_STATION"),
        ("ballots", "CANCELLED_BALLOT"),
    ]
    var_names = []
    for election_type, data in ELECTION_TYPES.items():
        election_type = election_type.upper()
        for subtype in data.get("subtypes", []):
            var_names.append("_".join([election_type, subtype["election_subtype"].upper(), "BALLOT"]))
        else:
            var_names.append("_".join([election_type, "BALLOT"]))
    all_data += [("ballots", var_name) for var_name in var_names]
    for voting_system in VOTING_SYSTEMS:
        voting_system = voting_system.upper().replace("-", "_")
        all_data.append(("ballots", f"{voting_system}_BALLOT"))

    parties = ["CON", "LAB", "GREEN", "LIBDEM", "REFORM", "INDEPENDENT"]
    for party in parties:
        all_data.append(("candidates", f"{party}_CANDIDATE"))

    for postcode in SANDBOX_POSTCODES:
        all_data.append(("sandbox", f"{postcode}_RESPONSE"))

    return all_data


@pytest.mark.parametrize("package_name,var_name", generate_expected_data())
def test_generated_responses_exist(package_name, var_name):
    module = importlib.import_module(f"response_builder.v1.generated_responses.{package_name}")
    klass = getattr(module, var_name, None)
    assert klass
    assert isinstance(klass, AbstractBuilder)
