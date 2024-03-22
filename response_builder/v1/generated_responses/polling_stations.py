from response_builder.v1.builders.polling_stations import (
    STOCK_POLLING_STATION_NO_MAP,
    PollingStationBuilder,
)

WITHOUT_MAP_POLLING_STATION = PollingStationBuilder().with_station(
    STOCK_POLLING_STATION_NO_MAP
)

WITH_MAP_POLLING_STATION = PollingStationBuilder().with_station()
