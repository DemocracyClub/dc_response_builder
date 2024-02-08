from response_builder.v1.builders.ballots import StockLocalBallotBuilder
from response_builder.v1.builders.base import RootBuilder
from response_builder.v1.generated_responses.root_responses import POLLING_STATION
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
