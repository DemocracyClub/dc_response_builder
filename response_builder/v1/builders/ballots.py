from response_builder.v1.builders.base import AbstractBuilder


class BallotBuilder(AbstractBuilder):
    pass


class LocalBallotBuilder(BallotBuilder):
    def with_candidate(self, candidate, **kwargs):
        # TODO
        ...
