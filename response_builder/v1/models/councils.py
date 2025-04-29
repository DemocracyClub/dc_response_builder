from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator


class ElectoralServices(BaseModel):
    council_id: str = Field(
        ..., description="Three letter code for this council"
    )
    name: str = Field(..., description="Name of this council")
    nation: str = Field(..., description="Name of nation")
    address: str = Field(..., description="Contact address for this council")
    postcode: str = Field(
        ...,
        description="Postcode component of contact address for this council",
    )
    email: Optional[EmailStr] = Field(
        ...,
        description="Contact email address for this council's Electoral Services team",
    )
    phone: str = Field(
        ...,
        description="Telephone number for this council's Electoral Services team",
    )
    website: Optional[HttpUrl] = Field(
        ..., description="URL for this council's website"
    )
    identifiers: List[str] = Field(
        ..., description="List of alternative identifiers for this council"
    )

    def __eq__(self, other: Any) -> bool:
        # TODO: Find a better way to do this, maybe by adding to the aggregator API?
        this_address = self.dict().get("address")
        try:
            other_address = other.dict()["address"]
        except AttributeError:
            return False
        return this_address == other_address

    @validator("email", pre=True, always=False)
    def validate_e(cls, val):
        if val == "":
            return None
        return val

    @validator("website", pre=True, always=False)
    def validate_website(cls, val: str):
        if not val:
            return ""
        if not val.startswith("http"):
            return f"https://{val}"
        return val


class Registration(BaseModel):
    """
    Sometimes the contact information for registration and proxy voting is
    different to the electoral services contact details. Use these if they
    exist and your users might have questions about voter registration.

    """

    address: str = Field(..., description="Contact address for this council")
    postcode: str = Field(
        ...,
        description="Postcode component of contact address for this council",
    )
    email: Optional[EmailStr] = Field(
        ...,
        description="Contact email address for this council's Electoral Services team",
    )
    phone: str = Field(
        ...,
        description="Telephone number for this council's Electoral Services team",
    )
    website: Optional[HttpUrl] = Field(
        ..., description="URL for this council's website"
    )

    @validator("email", pre=True, always=False)
    def validate_e(cls, val):
        if val == "":
            return None
        return val

    @validator("website", pre=True, always=False)
    def validate_website(cls, val: str):
        if not val:
            return ""
        if not val.startswith("http"):
            return f"https://{val}"
        return val

    def __eq__(self, other: Any) -> bool:
        this_address = self.dict().get("address")
        try:
            other_address = other.dict()["address"]
        except AttributeError:
            return False
        return this_address == other_address
