import datetime as dt
from typing import List

from uk_election_ids.datapackage import VOTING_SYSTEMS

from response_builder.v1.builders.base import AbstractBuilder
from response_builder.v1.models.base import (
    Ballot,
    Candidate,
    Timetable,
    VotingSystem,
)

REQUIRES_VOTER_ID = ["parl", "pcc", "mayor", "gla"]


def get_default_timetable(
    ballot_paper_id: str, poll_date: str, requires_id: bool
):
    """
    Generate a plausible-ish fake timetable
    ignoring a lot of complexity and nuance
    """

    polling_day = dt.date.fromisoformat(poll_date)

    notice_of_election_deadline = (
        polling_day - dt.timedelta(weeks=5)
    ).isoformat()

    if ballot_paper_id.startswith("ref."):
        close_of_nominations = None
        sopn_publish_deadline = None
    else:
        close_of_nominations = (polling_day - dt.timedelta(weeks=4)).isoformat()
        sopn_publish_deadline = (
            polling_day - dt.timedelta(weeks=4) + dt.timedelta(days=1)
        ).isoformat()

    registration_deadline = (polling_day - dt.timedelta(weeks=2)).isoformat()
    postal_vote_application_deadline = (
        polling_day - dt.timedelta(days=13)
    ).isoformat()

    vac_application_deadline = (
        (polling_day - dt.timedelta(weeks=1)).isoformat()
        if requires_id
        else None
    )

    return Timetable(
        notice_of_election_deadline=notice_of_election_deadline,
        close_of_nominations=close_of_nominations,
        sopn_publish_deadline=sopn_publish_deadline,
        registration_deadline=registration_deadline,
        postal_vote_application_deadline=postal_vote_application_deadline,
        vac_application_deadline=vac_application_deadline,
    )


class BallotBuilder(AbstractBuilder[Ballot]):
    model_class = Ballot

    def with_ballot_paper_id(self, ballot_paper_id):
        parts = ballot_paper_id.split(".")
        date = parts[-1]
        self.with_date(date)
        requires_id = any(
            election_type in ballot_paper_id
            for election_type in REQUIRES_VOTER_ID
        )

        if requires_id:
            self.with_voter_id_requirements(True)

        self.set("ballot_paper_id", ballot_paper_id)

        self.set(
            "timetable",
            get_default_timetable(ballot_paper_id, date, requires_id),
        )

        self.set(
            "wcivf_url",
            f"https://whocanivotefor.co.uk/elections/{ballot_paper_id}",
        )
        self.set(
            "ballot_url",
            f"https://developers.democracyclub.org.uk/api/v1/elections/{ballot_paper_id}",
        )
        return self

    def with_voter_id_requirements(self, requires_voter_id=False):
        self.set("requires_voter_id", requires_voter_id)
        return self

    def with_date(self, date):
        self.set("poll_open_date", date)
        return self

    def with_ballot_title(self, ballot_title):
        self.set("ballot_title", ballot_title)
        return self

    def with_post_name(self, post_name):
        self.set("post_name", post_name)
        return self

    def with_elected_role(self, elected_role):
        self.set("elected_role", elected_role)
        return self

    def with_election_name(self, election_name):
        self.set("election_name", election_name)
        return self

    def with_election_id(self, election_id):
        self.set("election_id", election_id)
        return self

    def with_voting_system(self, slug: str):
        self.set(
            "voting_system",
            VotingSystem(
                name=VOTING_SYSTEMS[slug]["name"],
                slug=slug,
                uses_party_lists=VOTING_SYSTEMS[slug]["uses_party_lists"],
            ).dict(),
        )
        return self

    def with_candidates(self, candidates=List[Candidate]):
        self.set("candidates_verified", True)
        self.set("candidates", candidates)
        return self

    def cancelled(self):
        self.set("cancelled", True)
        return self

    def with_cancellation_reason(self, reason):
        self.set("cancellation_reason", reason)
        return self.cancelled()

    def with_by_election_reason(self, reason):
        self.set("by_election_reason", reason)
        return self

    def with_notice_of_election_deadline(self, date: str):
        timetable = self._values.get("timetable", Timetable())
        timetable.notice_of_election_deadline = date
        self.set("timetable", timetable)
        return self

    def with_close_of_nominations(self, date: str):
        timetable = self._values.get("timetable", Timetable())
        timetable.close_of_nominations = date
        self.set("timetable", timetable)
        return self

    def with_registration_deadline(self, date: str):
        timetable = self._values.get("timetable", Timetable())
        timetable.registration_deadline = date
        self.set("timetable", timetable)
        return self

    def with_postal_vote_application_deadline(self, date: str):
        timetable = self._values.get("timetable", Timetable())
        timetable.postal_vote_application_deadline = date
        self.set("timetable", timetable)
        return self

    def with_vac_application_deadline(self, date: str):
        timetable = self._values.get("timetable", Timetable())
        timetable.vac_application_deadline = date
        self.set("timetable", timetable)
        return self


class LocalBallotBuilder(BallotBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.with_elected_role("Local councillor")
        self.with_voting_system("FPTP")


class ParlBallotBuilder(BallotBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.with_elected_role("MP")
        self.with_voting_system("FPTP")


class StockLocalBallotBuilder(LocalBallotBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.with_ballot_title("Stroud Slade local election")
        self.with_post_name("Stroud Slade")
        self.with_election_name("Stroud local elections")
        self.with_ballot_paper_id("local.stroud.stroud-slade.2024-05-02")
        self.with_election_id("local.stroud.2024-05-02")
