import datetime
from typing import List, Optional

from email_validator import validate_email
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    root_validator,
    validator,
)
from response_builder.v1.models.councils import ElectoralServices, Registration
from response_builder.v1.models.polling_stations import (
    AdvanceVotingStation,
    PollingStation,
)
from uk_election_ids.election_ids import IdBuilder


class Address(BaseModel):
    address: str = Field(
        description="The address of the property. This should be shown to users to pick"
    )
    postcode: str = Field(description="The postcode of the property")
    slug: str = Field(description="The UPRN of the property")
    url: str = Field(
        description="The URL to request (with authentication) to get information about the address"
    )


class Notification(BaseModel):
    type: str = Field(
        default_factory=str, description="The type of notification"
    )
    url: Optional[str] = Field(
        description=(
            "Details about this notification. This value should be shown "
            "to your users as a 'read more' link"
        ),
    )
    title: str = Field(
        description=(
            "A short title or heading for this notification. Designed to go "
            "in an approiate heading tag and be shown to users"
        )
    )
    detail: str = Field(
        description=(
            "A longer section of text, normally not more than a paragraph. "
            "This should be shown to users."
        )
    )


class Leaflet(BaseModel):
    leaflet_id: int = Field()
    thumb_url: Optional[HttpUrl] = Field()
    leaflet_url: Optional[HttpUrl] = Field()


class Party(BaseModel):
    party_name: str = Field()
    party_id: str = Field()


class Person(BaseModel):
    name: str = Field()
    ynr_id: int = Field()
    absolute_url: HttpUrl = Field()
    email: Optional[EmailStr] = Field()
    photo_url: Optional[HttpUrl] = Field()
    leaflets: Optional[List[Leaflet]]

    @validator("email", pre=True)
    def validate_email(cls, value):
        if not value:
            return
        try:
            validate_email(value)
        except ValueError:
            return None
        return value

class PreviousParty(BaseModel):
    ...


class Candidate(BaseModel):
    list_position: Optional[int] = Field()
    party: Party = Field()
    person: Person = Field()
    previous_party_affiliations: Optional[PreviousParty] = Field()


class VotingSystem(BaseModel):
    slug: str = Field()
    name: str = Field()


class Husting(BaseModel):
    title: str = Field()
    url: Optional[str] = Field()
    starts: Optional[str] = Field()
    ends: Optional[str] = Field()
    location: Optional[str] = Field()
    postevent_url: Optional[str] = Field(min_length=0)


class Ballot(BaseModel):
    ballot_paper_id: str = Field()
    ballot_title: str = Field()
    poll_open_date: datetime.date = Field()
    elected_role: str = Field()
    metadata: Optional[dict] = Field(default=None)
    cancelled: bool = Field(default=False)
    replaced_by: Optional[str] = Field()
    ballot_url: HttpUrl = Field()
    election_id: str = Field()
    election_name: str = Field()
    post_name: str = Field()
    candidates_verified: bool = Field(default=False)
    candidates: List[Candidate] = Field(default_factory=list)
    wcivf_url: HttpUrl = Field()
    voting_system: VotingSystem = Field()
    seats_contested: int = Field(default=1)
    hustings: Optional[List[Husting]] = Field(default=None)

    @validator("ballot_paper_id")
    def validate_ballot_paper_id(cls, value):
        election_id = IdBuilder.from_id(value)
        if not election_id.ballot_id == value:
            raise ValueError("Not a valid ballot_paper_id")
        return value


class Date(BaseModel):
    date: str = Field(
        default_factory=str, description="An ISO formatted date string"
    )
    polling_station: PollingStation = Field(
        default_factory=PollingStation,
        description="Information about the polling station for this date",
    )
    ballots: List[Ballot] = Field(
        default_factory=list, description="A list of ballots for this date"
    )
    advance_voting_station: Optional[AdvanceVotingStation] = Field(
        default_factory=None,
        description=(
            "(For Welsh ballots only) Indicates if there is an advance "
            "polling station, allowing voters to cast"
            "their ballot in person before polling day."
        ),
    )
    notifications: List[Notification] = Field(
        default_factory=list,
        description=(
            "A list of notifations that apply for this date. "
            "It's important these are shown to your users"
        ),
    )


class RootModel(BaseModel):
    address_picker: bool = Field(
        default=False,
        description=(
            "If true then the given postcode is 'split', meaning different "
            "addresses have different information. Pick an address from "
            "`addresses` and make a request to the URL given"
        ),
    )
    addresses: List[Address] = Field(
        default_factory=list,
        description="A list of addresses in this postcode. This list has commercial and other properties removed",
    )
    dates: List[Date] = Field(
        default_factory=list,
        description=(
            "A list of dates of elections that apply for this postcode. The dates are for elections that Democracy Club"
            "have marked as 'current', typically all future elections, and any election held in the past 30 days"
        ),
    )
    electoral_services: Optional[ElectoralServices] = Field(
        default_factory=None,
        description=(
            "Contact details for the user's local Electoral Services team. If we do not"
            " know the user's polling station, this can be used to provide contact info"
            " for their local council. This may be `null` if we are not able to"
            " determine the user's council."
        ),
        nullable=True,
    )
    registration: Optional[Registration] = Field(
        default_factory=None,
        description="""If this key is null, assume the electoral services contact 
        details can be used for electoral registration related enquiries.""",
        nullable=True,
    )

    @root_validator
    def not_address_picker_and_dates(cls, values):
        if values.get("address_picker") is True and values.get("dates"):
            raise ValueError("Can't add dates when address_picker=True")
        return values

    @classmethod
    def from_api_response(cls, api_response: dict) -> "RootModel":
        return cls.parse_obj(api_response)

    class Config:
        validate_assignment = True
