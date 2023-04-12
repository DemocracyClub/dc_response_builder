from response_builder.v1.builders import LocalBallotBuilder, RootBuilder
from response_builder.v1.factories.councils import NuneatonElectoralServices


def test_builder():
    builder = RootBuilder()
    ballot1 = LocalBallotBuilder()
    ballot1.with_candidates(3)
    builder.with_ballot(ballot1.build())
    # builder.with_ballot(ballot2)
    builder.with_electoral_services(NuneatonElectoralServices)
    print(builder.build().json(indent=4))
