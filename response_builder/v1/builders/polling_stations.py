from response_builder.v1.builders.base import AbstractBuilder
from response_builder.v1.models.polling_stations import PollingStation


class PollingStationBuilder(AbstractBuilder[PollingStation]):
    model_class = PollingStation
