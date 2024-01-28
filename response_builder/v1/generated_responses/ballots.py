from response_builder.v1.builders import LocalBallotBuilder  # noqa

SINGLE_LOCAL_BALLOT = LocalBallotBuilder().with_candidates(1, verified=False)
