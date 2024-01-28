from response_builder.v1.factories.ballots import LocalElectionBallotFactory
from response_builder.v1.factories.candidates import CandidateFactory
from response_builder.v1.models.base import Ballot

from v1.builders.base import AbstractBuilder


class BallotBuilder(AbstractBuilder):
    pass


class LocalBallotBuilder(BallotBuilder):
    factory: Ballot = LocalElectionBallotFactory

    def with_candidates(self, count, verified=False):
        self.factory.candidates_verified = verified
        self.factory.seats_contested = 1
        for i in range(count):
            self.with_candidate()
        return self

    def with_candidate(self, candidate=None, **kwargs):
        if not candidate:
            candidate = CandidateFactory().build(**kwargs)
        if not hasattr(self.factory, "candidates"):
            self.factory.candidates = []
        self.factory.candidates.append(candidate)
        return self
