from response_builder.v1.builders.ballots import (
    StockLocalBallotBuilder,
)
from response_builder.v1.builders.base import RootBuilder
from response_builder.v1.generated_responses import (
    candidates,
    electoral_services,
)
from response_builder.v1.generated_responses.ballots import (
    GLA_BALLOT,
    LOCAL_BALLOT,
    MAYOR_BALLOT,
    PARL_BALLOT,
    PCC_BALLOT,
)
from response_builder.v1.generated_responses.candidates import (
    CON_CANDIDATE,
    GREEN_CANDIDATE,
)
from response_builder.v1.generated_responses.polling_stations import (
    WITHOUT_MAP_POLLING_STATION,
)
from response_builder.v1.models.base import CancellationReason

# < -- root responses -- >
NO_LOCAL_BALLOTS = RootBuilder().with_electoral_services(
    electoral_services.stroud_electoral_services
)

RECENTLY_PASSED_LOCAL_BALLOT = RootBuilder().with_ballot(
    StockLocalBallotBuilder(
        poll_open_date="2024-03-01",
        ballot_paper_id="local.stroud.2024-03-01",
    ).build()
)

SINGLE_LOCAL_FUTURE_BALLOT_WITH_POLLING_STATION = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_candidates(candidates.all_candidates)
        .build()
    )
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

SINGLE_LOCAL_FUTURE_BALLOT_WITHOUT_POLLING_STATION = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_candidates(candidates.all_candidates)
        .build()
    )
    .without_polling_station()
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

SINGLE_LOCAL_FUTURE_BALLOT_WITH_ADDRESS_PICKER = (
    RootBuilder()
    .with_ballot(
        LOCAL_BALLOT.with_candidates(candidates.all_candidates).build()
    )
    .with_address_picker()
    .with_electoral_services(electoral_services.wandsworth_electoral_services)
)

MULTIPLE_BALLOTS_WITH_VOTING_SYSTEM_AND_POLLING_STATION = (
    RootBuilder()
    .with_multiple_ballots(
        [
            MAYOR_BALLOT.with_candidates(candidates.all_candidates).build(),
            GLA_BALLOT.with_candidates(candidates.all_candidates).build(),
        ]
    )
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.stroud_electoral_services)
)



PARL_RESPONSE = (
    RootBuilder()
    .with_ballot(PARL_BALLOT.build())
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

GLA_RESPONSE = (
    RootBuilder()
    .with_ballot(StockLocalBallotBuilder().build())
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.wandsworth_electoral_services)
)

PCC_RESPONSE = (
    RootBuilder()
    .with_ballot(PCC_BALLOT.build())
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

MAYORAL_RESPONSE = (
    RootBuilder()
    .with_ballot(MAYOR_BALLOT.build())
    .with_polling_station(WITHOUT_MAP_POLLING_STATION.build())
    .with_electoral_services(electoral_services.wandsworth_electoral_services)
)

CANCELLED_BALLOT_CANDIDATE_DEATH = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_cancellation_reason(CancellationReason.CANDIDATE_DEATH)
        .build()
    )
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

CANCELLED_BALLOT_NO_CANDIDATES = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_cancellation_reason(CancellationReason.NO_CANDIDATES)
        .build()
    )
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

CANCELLED_BALLOT_EQUAL_CANDIDATES = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_cancellation_reason(CancellationReason.EQUAL_CANDIDATES)
        .set("seats_contested", 2)
        .with_candidates([GREEN_CANDIDATE, CON_CANDIDATE])
        .build()
    )
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

CANCELLED_BALLOT_UNDER_CONTESTED = (
    RootBuilder()
    .with_ballot(
        StockLocalBallotBuilder()
        .with_cancellation_reason(CancellationReason.UNDER_CONTESTED)
        .set("seats_contested", 3)
        .with_candidates([GREEN_CANDIDATE, CON_CANDIDATE])
        .build()
    )
    .with_electoral_services(electoral_services.stroud_electoral_services)
)

ONE_CANCELLED_BALLOT_ONE_NOT = (
    RootBuilder()
    .with_ballot(
        PARL_BALLOT.with_date(
            StockLocalBallotBuilder()._values["poll_open_date"]
        ).build()
    )
    .with_ballot(
        StockLocalBallotBuilder()
        .with_cancellation_reason(CancellationReason.UNDER_CONTESTED)
        .set("seats_contested", 3)
        .with_candidates([GREEN_CANDIDATE, CON_CANDIDATE])
        .build()
    )
    .with_electoral_services(electoral_services.stroud_electoral_services)
)


MULTIPLE_BALLOTS_WITH_CANCELLATION = RootBuilder().with_multiple_ballots(
    [
        MAYOR_BALLOT.build(),
        PARL_BALLOT.build(),
        GLA_BALLOT.build(),
        StockLocalBallotBuilder().with_cancellation_reason(reason=CancellationReason.CANDIDATE_DEATH).build(),
    ]
).with_electoral_services(electoral_services.stroud_electoral_services)
