from uk_election_ids.datapackage import VOTING_SYSTEMS

from response_builder.v1.builders.base import AbstractBuilder
from response_builder.v1.models.base import Ballot, VotingSystem


class BallotBuilder(AbstractBuilder[Ballot]):
    model_class = Ballot

    def with_ballot_paper_id(self, ballot_paper_id):
        parts = ballot_paper_id.split(".")
        date = parts[-1]
        self.with_date(date)
        self.set("ballot_paper_id", ballot_paper_id)
        self.set(
            "wcivf_url",
            f"https://whocanivotefor.co.uk/elections/{ballot_paper_id}",
        )
        self.set(
            "ballot_url",
            f"https://developers.democracyclub.org.uk/api/v1/elections/{ballot_paper_id}",
        )
        return self

    def with_date(self, date):
        self.set("poll_open_date", date)
        return self

    def with_voting_system(self, voting_system_slug):
        voting_system = VotingSystem(
            slug=voting_system_slug, **VOTING_SYSTEMS.get(voting_system_slug)
        )
        self.set("voting_system", voting_system)

    def with_ballot_title(self, ballot_title):
        self.set("ballot_title", ballot_title)
        return self

    def with_post_name(self, post_name):
        self.set("post_name", post_name)
        return self

    def with_election_name(self, election_name):
        self.set("election_name", election_name)
        return self

    def with_election_id(self, election_id):
        self.set("election_id", election_id)
        return self


class LocalBallotBuilder(BallotBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set("elected_role", "Local councillor")


class StockLocalBallotBuilder(LocalBallotBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.with_ballot_title("Stroud Slade local election")
        self.with_post_name("Stroud Slade")
        self.with_election_name("Stroud local elections")
        self.with_voting_system("FPTP")
        self.with_ballot_paper_id("local.stroud.slade.2024-02-20")
        self.with_election_id("local.stroud.2024-02-28")

    def with_division(self, param):
        return self
