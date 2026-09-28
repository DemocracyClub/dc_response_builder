import datetime as dt
import importlib

import pytest
from uk_election_ids.datapackage import ELECTION_TYPES, VOTING_SYSTEMS

from response_builder.v1.builders.ballots import StockLocalBallotBuilder
from response_builder.v1.builders.base import AbstractBuilder, RootBuilder
from response_builder.v1.generated_responses.polling_stations import (
    WITHOUT_MAP_POLLING_STATION,
)
from response_builder.v1.models.base import Candidate, RootModel


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
        "postcode_location": {
            "geometry": {"coordinates": [], "type": "Point"},
            "properties": None,
            "type": "Feature",
        },
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
    builder.with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    built = builder.build()
    assert not built.address_picker
    assert built.dates
    assert built.dates[0].polling_station.polling_station_known

    # Now add an address picker
    builder.with_address_picker()
    built = builder.build()
    assert built.address_picker
    assert not built.dates


def test_set_date_baseline_moves_date_and_ballot_fields():
    ballot = StockLocalBallotBuilder().build()
    builder = RootBuilder().with_ballot(ballot)

    builder.set_date_baseline("2030-01-01")

    built = builder.build()
    assert built.dates[0].date == "2030-01-01"
    moved_ballot = built.dates[0].ballots[0]
    assert moved_ballot.poll_open_date == dt.date(2030, 1, 1)
    assert (
        moved_ballot.ballot_paper_id == "local.stroud.stroud-slade.2030-01-01"
    )
    assert moved_ballot.election_id == "local.stroud.2030-01-01"


def test_set_date_baseline_accepts_date_object():
    ballot = StockLocalBallotBuilder().build()
    builder = RootBuilder().with_ballot(ballot)

    builder.set_date_baseline(dt.date(2030, 1, 1))

    assert builder.build().dates[0].date == "2030-01-01"


def test_set_date_baseline_preserves_gap_between_multiple_dates():
    ballot1 = StockLocalBallotBuilder().build()
    ballot2 = (
        StockLocalBallotBuilder()
        .with_ballot_paper_id("local.stroud.stroud-slade.2024-06-06")
        .with_election_id("local.stroud.2024-06-06")
        .build()
    )
    builder = RootBuilder().with_multiple_ballots([ballot1, ballot2])

    builder.set_date_baseline("2030-01-01")

    built = builder.build()
    assert built.dates[0].date == "2030-01-01"
    # original gap between ballot1 and ballot2 was 35 days
    assert built.dates[1].date == "2030-02-05"


def test_set_date_baseline_is_noop_with_address_picker():
    builder = (
        RootBuilder()
        .with_ballot(StockLocalBallotBuilder().build())
        .with_address_picker()
    )

    result = builder.set_date_baseline("2030-01-01")

    assert result is builder
    assert builder.build().dates == []


def test_set_date_baseline_raises_without_dates():
    builder = RootBuilder()

    with pytest.raises(ValueError):
        builder.set_date_baseline("2030-01-01")


def generate_expected_data():
    # Ballots
    all_data = [
        ("polling_stations", "WITH_MAP_POLLING_STATION", AbstractBuilder),
        ("polling_stations", "WITHOUT_MAP_POLLING_STATION", AbstractBuilder),
        ("ballots", "CANCELLED_BALLOT", AbstractBuilder),
    ]
    var_names = []
    for election_type, data in ELECTION_TYPES.items():
        election_type = election_type.upper()
        # TODO: Add these examples in
        if election_type in ["NIA", "NAW", "SENEDD", "SP", "EUROPARL"]:
            continue
        for subtype in data.get("subtypes", []):
            var_names.append(
                "_".join(
                    [
                        election_type,
                        subtype["election_subtype"].upper(),
                        "BALLOT",
                    ]
                )
            )
        else:
            var_names.append("_".join([election_type, "BALLOT"]))
    all_data += [
        ("ballots", var_name, AbstractBuilder) for var_name in var_names
    ]
    for voting_system in VOTING_SYSTEMS:
        voting_system = voting_system.upper().replace("-", "_")
        all_data.append(("ballots", f"{voting_system}_BALLOT", AbstractBuilder))

    parties = ["CON", "LAB", "GREEN", "LIBDEM", "REFORM", "INDEPENDENT"]
    for party in parties:
        all_data.append(("candidates", f"{party}_CANDIDATE", Candidate))

    # TODO: add these in
    # for postcode in SANDBOX_POSTCODES:
    #     all_data.append(("sandbox", f"{postcode}_RESPONSE", AbstractBuilder))

    return all_data


@pytest.mark.parametrize(
    "package_name,var_name,klass_type", generate_expected_data()
)
def test_generated_responses_exist(package_name, var_name, klass_type):
    module = importlib.import_module(
        f"response_builder.v1.generated_responses.{package_name}"
    )
    klass = getattr(module, var_name, None)
    assert klass
    assert isinstance(klass, klass_type)
