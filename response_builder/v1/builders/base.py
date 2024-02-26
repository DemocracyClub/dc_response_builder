from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from response_builder.v1.models.base import Ballot, Date, RootModel
from response_builder.v1.models.councils import ElectoralServices
from response_builder.v1.models.polling_stations import PollingStation

ModelType = TypeVar("ModelType", bound=BaseModel)


class AbstractBuilder(Generic[ModelType]):
    model_class: Optional[Type[BaseModel]] = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._values = {}

    def set(self, key, value):
        if key not in self.model_class.__fields__:
            raise ValueError(
                f'"{key}" is not a valid attribute name for "{self.model_class.__name__}".'
            )
        known_field = self.model_class.__fields__[key]
        dict_without_original_value = {
            k: v for k, v in self.model_class.__dict__.items() if k != key
        }
        value, error_ = known_field.validate(
            value,
            dict_without_original_value,
            loc=key,
            cls=self.model_class.__class__,
        )
        if error_:
            raise ValidationError([error_], self.__class__)
        self._values[key] = value
        return self

    def build(self, **kwargs) -> ModelType:
        return self.model_class(**self._values)


class RootBuilder(AbstractBuilder[RootModel]):
    model_class = RootModel

    def with_address_picker(self):
        self.set("address_picker", True)
        self._values.pop("dates", None)
        return self

    def with_date(self, date_model: Optional[Date] = None):
        if "dates" not in self._values:
            self._values["dates"] = []
        existing_dates = self._values["dates"]
        existing_dates.append(date_model)
        self.set("dates", existing_dates)
        return self

    def with_ballot(self, ballot_model: Ballot):
        """
        Convince class for adding a ballot inside a date object.

        The date of the ballot is added to the dates array
        """
        if self._values.get("address_picker"):
            return self
        ballot_date = ballot_model.poll_open_date
        date_model = Date(date=str(ballot_date))
        date_model.ballots.append(ballot_model)
        self.with_date(date_model)
        return self

    def with_electoral_services(self, electoral_services: ElectoralServices):
        self.set("electoral_services", electoral_services)
        return self

    def with_polling_station(self, polling_station: PollingStation):
        if not self._values["dates"]:
            raise ValueError("Can't add polling station with no dates")
        date = self._values["dates"][0]
        date.polling_station = polling_station
        return self
    
    def without_polling_station(self):
        if not self._values["dates"]:
            raise ValueError("Can't add polling station with no dates")
        date = self._values["dates"][0]
        date.polling_station = PollingStation() 
        return self
        return self
