from response_builder.v1.builders.base import AbstractBuilder
from response_builder.v1.models.polling_stations import (
    PollingStation,
    Station,
    StationProperties,
)

STOCK_POLLING_STATION_NO_MAP = Station(
    id="AA1",
    type="station",
    properties=StationProperties(
        address="Stroud Valley Scouting Centre\nChapel Street\nStroud",
        postcode="GL5 1DU",
    ),
)

STOCK_POLLING_STATION_WITH_MAP = Station(
    id="AA1", type="station", properties=StationProperties(address="Foo Bar")
)


class PollingStationBuilder(AbstractBuilder[PollingStation]):
    model_class = PollingStation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set("polling_station_known", True)

    def with_station(self, station=STOCK_POLLING_STATION_WITH_MAP):
        self.set("station", station)
        return self
