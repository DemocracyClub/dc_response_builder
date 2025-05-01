import pytest

from response_builder.v1.generated_responses import (
    ballots,
    polling_stations,
    root_responses,
)

responses = [
    # ballots
    ballots.LOCAL_BALLOT,
    ballots.PARL_BALLOT,
    ballots.GLA_BALLOT,
    ballots.PCC_BALLOT,
    ballots.MAYOR_BALLOT,
    # stations
    polling_stations.WITHOUT_MAP_POLLING_STATION,
    polling_stations.WITH_MAP_POLLING_STATION,
    # full responses
    root_responses.CANCELLED_BALLOT_CANDIDATE_DEATH,
    root_responses.CANCELLED_BALLOT_EQUAL_CANDIDATES,
    root_responses.CANCELLED_BALLOT_NO_CANDIDATES,
    root_responses.CANCELLED_BALLOT_UNDER_CONTESTED,
    root_responses.GLA_RESPONSE,
    root_responses.MAYORAL_RESPONSE,
    root_responses.MULTIPLE_BALLOTS_WITH_CANCELLATION,
    root_responses.MULTIPLE_BALLOTS_WITH_VOTING_SYSTEM_AND_POLLING_STATION,
    root_responses.NO_LOCAL_BALLOTS,
    root_responses.ONE_CANCELLED_BALLOT_ONE_NOT,
    root_responses.PARL_RESPONSE,
    root_responses.PCC_RESPONSE,
    root_responses.RECENTLY_PASSED_LOCAL_BALLOT,
    root_responses.SINGLE_LOCAL_FUTURE_BALLOT_WITHOUT_POLLING_STATION,
    root_responses.SINGLE_LOCAL_FUTURE_BALLOT_WITH_ADDRESS_PICKER,
    root_responses.SINGLE_LOCAL_FUTURE_BALLOT_WITH_POLLING_STATION,
    root_responses.WITHOUT_MAP_POLLING_STATION,
]


@pytest.mark.parametrize("response", responses)
def test_responses(response):
    assert response.build()
