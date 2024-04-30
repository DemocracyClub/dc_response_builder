from response_builder.v1.models.base import (
    Candidate,
    EmailStr,
    Leaflet,
    Party,
    Person,
    PreviousParty,
)

LAB_CANDIDATE = Candidate(
    list_position=3,
    party=Party(
        party_name="Labour Party",
        party_id="PP53",
    ),
    person=Person(
        name="Mr. Foo Bar",
        ynr_id=123,
        absolute_url="https://candidates.democracyclub.org.uk/person/123",
        email=EmailStr("person@website.com"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/123/fc123.jpg",
        leaflets=[
            Leaflet(
                leaflet_id=123,
                thumb_url="https://electionleaflets.org/leaflets/123/",
                leaflet_url="https://electionleaflets.org/leaflets/123/",
            )
        ],
    ),
    previous_party_affiliations=[
        PreviousParty(party_name="Liberal Democrats", party_id="PP90")
    ],
)

CON_CANDIDATE = Candidate(
    list_position=1,
    party=Party(
        party_name="Conservative Party",
        party_id="PP52",
    ),
    person=Person(
        name="Mrs. Bar Foo",
        ynr_id=456,
        absolute_url="https://candidates.democracyclub.org.uk/person/456",
        email=EmailStr("person2@website.com"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/456/fc456.jpg",
        leaflets=[
            Leaflet(
                leaflet_id=456,
                thumb_url="https://electionleaflets.org/leaflets/456/",
                leaflet_url="https://electionleaflets.org/leaflets/456/",
            )
        ],
    ),
    previous_party_affiliations=[
        PreviousParty(party_name="Liberal Democrats", party_id="PP90")
    ],
)

LIBDEM_CANDIDATE = Candidate(
    list_position=2,
    party=Party(
        party_name="Liberal Democrats Party",
        party_id="PP90",
    ),
    person=Person(
        name="Dr. Baz Qux",
        ynr_id=123,
        absolute_url="https://candidates.democracyclub.org.uk/person/789",
        email=EmailStr("dr_person@website.com"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/789/fc789.jpg",
        leaflets=[
            Leaflet(
                leaflet_id=789,
                thumb_url="https://electionleaflets.org/leaflets/789/",
                leaflet_url="https://electionleaflets.org/leaflets/789/",
            )
        ],
    ),
    previous_party_affiliations=[
        PreviousParty(party_name="Liberal Democrats", party_id="PP90")
    ],
)

GREEN_CANDIDATE = Candidate(
    list_position=4,
    party=Party(
        party_name="Green Party",
        party_id="PP24",
    ),
    person=Person(
        name="Ms. Qux Baz",
        ynr_id=101112,
        absolute_url="https://candidates.democracyclub.org.uk/person/101112",
        email=EmailStr("green@greenparty.co.uk"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/101112/fc101112.jpg",
        leaflets=[
            Leaflet(
                leaflet_id=101112,
                thumb_url="https://electionleaflets.org/leaflets/101112/",
                leaflet_url="https://electionleaflets.org/leaflets/101112/",
            )
        ],
    ),
    previous_party_affiliations=[
        PreviousParty(party_name="Liberal Democrats", party_id="PP90")
    ],
)

INDEPENDENT_CANDIDATE = Candidate(
    list_position=4,
    party=Party(
        party_name="Independent",
        party_id="ynmp-party:2",
    ),
    person=Person(
        name="Ms. Qux Baz",
        ynr_id=101112,
        absolute_url="https://candidates.democracyclub.org.uk/person/101112",
        email=EmailStr("independent@example.com"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/101112/fc101112.jpg",
    ),
)
REFORM_CANDIDATE = Candidate(
    list_position=4,
    party=Party(
        party_name="Reform",
        party_id="PP7931",
    ),
    person=Person(
        name="Ms. Qux Baz",
        ynr_id=101112,
        absolute_url="https://candidates.democracyclub.org.uk/person/101112",
        email=EmailStr("independent@example.com"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/101112/fc101112.jpg",
    ),
)

ni_candidate = Candidate(
    list_position=5,
    party=Party(
        party_name="Irish Republican Socialist Party",
        party_id="PP14057",
    ),
    person=Person(
        name="Mr. Ni Irsp",
        ynr_id=131415,
        absolute_url="https://candidates.democracyclub.org.uk/person/131415",
        email=EmailStr("ni@irsp.co.uk"),
        photo_url="https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/cache/fc/131415/fc131415.jpg",
        leaflets=[
            Leaflet(
                leaflet_id=456,
                thumb_url="https://electionleaflets.org/leaflets/131415/",
                leaflet_url="https://electionleaflets.org/leaflets/131415/",
            )
        ],
    ),
    previous_party_affiliations=[
        PreviousParty(
            party_name="Irish Republican Socialist Party", party_id="PP123"
        )
    ],
)

# make a list of candidates
all_candidates = [
    LAB_CANDIDATE,
    CON_CANDIDATE,
    LIBDEM_CANDIDATE,
    GREEN_CANDIDATE,
    ni_candidate,
]
# make a list of just the labour candidate
labour_candidates = [LAB_CANDIDATE]
