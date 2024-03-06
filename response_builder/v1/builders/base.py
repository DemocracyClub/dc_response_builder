from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError
from uk_election_ids.metadata_tools import VotingSystemMatcher
from uk_election_ids.datapackage import VOTING_SYSTEMS


from response_builder.v1.models.base import (
    Ballot,
    Date,
    RootModel,
    VotingSystem,
    Address,
    Candidate,
    Party,
    Person,
    Candidate,
    Leaflet,
    PreviousParty,
    EmailStr,
    PreviousParty,
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
    
    def with_multiple_ballots(self, ballot_models: list[Ballot]):
        for ballot in ballot_models:
            # there may be a cancellation and this will fail
            try: 
                self.with_ballot(ballot)
            except Exception as e:
                print(e)
                continue
        return self
    
    def without_ballot(self):
        self._values.pop("dates", None)
        return self

    def with_candidates(self, candidates = list[Candidate]):
        if not self._values["dates"]:
            raise ValueError("Can't add candidates with no dates")

        date = self._values["dates"][0]
        for ballot in date.ballots:
            ballot.candidates = candidates
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
    
    def with_cancelled(self):
        if not self._values["dates"]:
            raise ValueError("Can't cancel a ballot with no dates")
        ballot = self._values["dates"][0].ballots[0]
        ballot.cancelled = True    
        # This needs a notification update, 
        # but there is a conflict between 
        # expectations of list vs dict
        return self
         
    def with_voting_system(self, voting_system: str, nation: str = "England"):
        if not self._values["dates"]:
            raise ValueError("Can't set a voting_system on a ballot with no dates")
        date = self._values["dates"][0]
        for ballot in date.ballots:
            election_id = ballot.ballot_paper_id
            nation = "ENG" 
            voting_system = VotingSystemMatcher(election_id, nation).get_voting_system()
            voting_system = VotingSystem(name=VOTING_SYSTEMS[voting_system]["name"], slug=voting_system)
            self.set("voting_system", voting_system)
        return self