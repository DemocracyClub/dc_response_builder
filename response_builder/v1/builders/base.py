from datetime import date, datetime
from typing import Generic, List, Optional, Type, TypeVar, Union

from dateutil.parser import parse
from pydantic import BaseModel, ValidationError

from response_builder.v1.models.base import (
    Address,
    Ballot,
    Date,
    RootModel,
)
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
        self.set("addresses", [])

        self._values.pop("dates", None)

        address1 = Address(
            address="1 Foo Street",
            postcode="AA1 1AA",
            slug="10035187881",
            url="https://foo-street",
        )
        address2 = Address(
            address="2 Bar Street",
            postcode="AA1 1AB",
            slug="10035187882",
            url="https://bar-street",
        )
        address3 = Address(
            address="3 Baz Street",
            postcode="AA1 1AC",
            slug="10035187883",
            url="https://baz-street",
        )
        self._values["addresses"].append(address1)
        self._values["addresses"].append(address2)
        self._values["addresses"].append(address3)
        return self

    def with_date(self, date_model: Optional[Date] = None):
        if "dates" not in self._values:
            self._values["dates"] = []
        existing_dates: List = self._values["dates"]
        matching_dates = [
            existing_date_model
            for existing_date_model in existing_dates
            if existing_date_model.date == date_model.date
        ]
        if matching_dates:
            existing_dates.remove(matching_dates[0])
            existing_dates.append(date_model)
        else:
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
        ballot_date = str(ballot_model.poll_open_date)
        matching_dates = [
            date_model
            for date_model in self._values.get("dates", [])
            if date_model.date == ballot_date
        ]
        if matching_dates:
            date_model = matching_dates[0]
        else:
            date_model = Date(date=ballot_date)
        date_model.ballots.append(ballot_model)
        return self.with_date(date_model)

    def with_multiple_ballots(self, ballot_models: List[Ballot]):
        modified = self
        for ballot in ballot_models:
            # there may be a cancellation and this will fail
            modified = modified.with_ballot(ballot)
        return modified

    def without_ballot(self):
        self._values.pop("dates", None)
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

    def set_date_baseline(self, new_date: Union[date, str]):
        """
        For dynamically updating dates of ballots.

        Because it's useful to test responses at various points over an election timetable
        we can set the dates for a response to any date.

        The "baseline" is the first election date in self.dates. That is, the earliest election
        we will see.

        For example, if we have 3 upcoming elections in a response:

        2018-05-03
        2018-06-07
        2018-06-21

        and we called set_date_baseline(2022-01-02) the election dates would be changed to:

        2022-01-02
        2022-02-03
        2022-02-17

        """
        if self._values.get("address_picker"):
            return self

        if isinstance(new_date, str):
            new_date = parse(new_date).date()

        if not self._values.get("dates", None):
            raise ValueError("No dates to change")

        baseline = parse(self._values["dates"][0].date).date()
        delta = new_date - baseline
        for date_model in self._values["dates"]:
            updated_date = (
                (datetime.fromisoformat(date_model.date) + delta)
                .date()
                .isoformat()
            )
            date_model.date = updated_date
            for ballot in date_model.ballots:
                ballot.poll_open_date = updated_date
                parts = ballot.ballot_paper_id.split(".")
                parts[-1] = str(updated_date)
                ballot.ballot_paper_id = ".".join(parts)

                parts = ballot.election_id.split(".")
                parts[-1] = str(updated_date)
                ballot.election_id = ".".join(parts)
        return self
