from response_builder.v1.builders.ballots import StockLocalBallotBuilder
from response_builder.v1.builders.base import RootBuilder
from response_builder.v1.builders.polling_stations import PollingStationBuilder
from response_builder.v1.models.polling_stations import Station, StationProperties

SINGLE_LOCAL_FUTURE_BALLOT = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()
)

POLLING_STATION = (
    PollingStationBuilder().set("polling_station_known", True).build()
)
POLLING_STATION.station = Station(id="AA1", type="station", properties=StationProperties(address="Foo Bar"))

SINGLE_LOCAL_FUTURE_BALLOT_WITH_POLLING_STATION = (
    SINGLE_LOCAL_FUTURE_BALLOT.with_polling_station(POLLING_STATION)
)
