import json

import pytest
from pydantic import ValidationError

from response_builder.v1.generated_responses import ballots
from response_builder.v1.models.base import (
    Ballot,
    Date,
    PostcodeLocation,
    RootModel,
)
from response_builder.v1.models.common import Point
from response_builder.v1.models.councils import ElectoralServices, Registration


def test_electoral_services_eq_registration():
    kwargs = {
        "council_id": "ABC",
        "name": "Council",
        "nation": "Council",
        "address": "address",
        "postcode": "SW1A 1AA",
        "phone": "123456",
        "email": "foo@bar.gov.uk",
        "website": "https://example.com",
        "identifiers": [],
    }

    reg = Registration(**kwargs)
    es = ElectoralServices(**kwargs)

    assert es == reg
    assert reg == es

    other_reg = Registration(**kwargs)
    other_reg.address = "NOT THE SAME"

    assert es != other_reg
    assert es != "foo"
    assert reg != "foo"


def test_root_model():
    model = RootModel(
        postcode_location=PostcodeLocation(
            geometry=Point(coordinates=[], type="Point"), type="Feature"
        )
    )

    model.dates = [Date(date="2021-05-04")]

    data = """
    {
  "address_picker": false,
  "addresses": [],
  "dates": [
    {
      "date": "2018-05-03",
      "polling_station": {
        "polling_station_known": false,
        "custom_finder": "http://www.eoni.org.uk/Offices/Postcode-Search-Results?postcode=BT28%202EY",
        "report_problem_url": null,
        "station": null
      },
      "advance_voting_station": null,
      "notifications": [
        {
          "type": "voter_id",
          "url": "http://www.eoni.org.uk/Vote/Voting-at-a-polling-place",
          "title": "You need to show photographic ID to vote in this election",
          "detail": "Voters in Northern Ireland are required to show one form of photo ID, like a passport or driving licence."
        }
      ],
      "ballots": [
        {
          "ballot_paper_id": "parl.west-tyrone.by.2018-05-03",
          "ballot_title": "West Tyrone by-election",
          "ballot_url": "https://developers.democracyclub.org.uk/api/v1/sandbox/elections/parl.west-tyrone.by.2018-05-03/",
          "poll_open_date": "2018-11-22",
          "elected_role": "Member of Parliament",
          "metadata": {
            "ni-voter-id": {
              "url": "http://www.eoni.org.uk/Vote/Voting-at-a-polling-place",
              "title": "You need to show photographic ID to vote in this election",
              "detail": "Voters in Northern Ireland are required to show one form of photo ID, like a passport or driving licence."
            }
          },
          "cancelled": false,
          "replaced_by": null,
          "replaces": null,
          "election_id": "parl.2018-05-03",
          "election_name": "UK Parliament elections",
          "post_name": "West Tyrone",
          "candidates_verified": false,
          "voting_system": {
            "slug": "FPTP",
            "name": "First-past-the-post",
            "uses_party_lists": false
          },
          "hustings": [
            {
              "title": "Local elections hustings",
              "url": "https://example.com/hustings/",
              "starts": "2018-04-28T18:00:00Z",
              "ends": "2018-04-28T20:30:00Z",
              "location": "Westminster Hall",
              "postevent_url": "https://example.com/hustings/"
            }
          ],
          "seats_contested": 1,
          "candidates": [],
          "wcivf_url": "https://whocanivotefor.co.uk/elections/parl.2018-05-03/post-WMC:N06000018/west-tyrone"
        }
      ]
    }
  ],
  "electoral_services": {
    "council_id": "ABC",
    "name": "",
    "nation": "Northern Ireland",
    "email": "info@eoni.org.uk",
    "phone": "",
    "website": "http://www.eoni.org.uk/",
    "postcode": "BT1 1ER",
    "address": "The Electoral Office Headquarters St Anne's House 15 Church Street Belfast",
    "identifiers": ["N09000007"]
  },
  "registration": {
    "email": "info@eoni.org.uk",
    "phone": "",
    "website": "http://www.eoni.org.uk/",
    "postcode": "BT1 1ER",
    "address": "The Electoral Office Headquarters St Anne's House 15 Church Street Belfast"
  },
  "postcode_location": {
    "type": "Feature",
    "properties": null,
    "geometry": {
      "type": "Point",
      "coordinates": [
        -6.206229,
        54.550429
      ]
    }
  }
}


"""

    assert model.validate(json.loads(data))


def test_ballot_with_elected_role():
    ballot = Ballot(**ballots.LOCAL_BALLOT.build().dict())
    assert ballot.elected_role == "Local councillor"


def test_missing_elected_role():
    data = ballots.LOCAL_BALLOT.build().dict()
    data.pop("elected_role")
    with pytest.raises(ValidationError) as excinfo:
        Ballot(**data)
    assert "elected_role must be provided" in str(excinfo.value)


def test_elected_role_referendum():
    data = ballots.REF_BALLOT.build().dict()
    ballot = Ballot(**data)
    assert ballot.elected_role is None
