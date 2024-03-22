from response_builder.v1.builders.ballots import (
    BallotBuilder,
    ParlBallotBuilder,
    StockLocalBallotBuilder,
)
from response_builder.v1.generated_responses import candidates

LOCAL_BALLOT = StockLocalBallotBuilder()
PARL_BALLOT = (
    ParlBallotBuilder()
    .with_ballot_title("Stroud parliamentary by-election")
    .with_post_name("Stroud constituency")
    .with_election_name("Stroud constituency")
    .with_ballot_paper_id("parl.stroud.2024-11-14")
    .with_election_id("parl.stroud.2024-11-14")
    .with_candidates(candidates.all_candidates)
)
GLA_BALLOT = (
    StockLocalBallotBuilder()
    .with_ballot_title("London Assembly elections")
    .with_post_name("London Assembly")
    .with_election_name("London Assembly elections")
    .with_ballot_paper_id("gla.a.2024-05-02")
    .with_election_id("gla.a.2024-05-02")
)
GLA_C_BALLOT = BallotBuilder()
GLA_A_BALLOT = BallotBuilder()
PR_CL_BALLOT = BallotBuilder()
STV_BALLOT = BallotBuilder()
SV_BALLOT = BallotBuilder()
FPTP_BALLOT = BallotBuilder()
PCC_BALLOT = (
    StockLocalBallotBuilder()
    .with_ballot_title("Police and Crime Commissioner elections")
    .with_post_name("Police and Crime Commissioner for Avon and Somerset")
    .with_election_name("Police and Crime Commissioner election")
    .with_ballot_paper_id("pcc.avon-and-somerset.2024-05-02")
    .with_election_id("pcc.avon-and-somerset.2024-05-02")
)
MAYOR_BALLOT = (
    StockLocalBallotBuilder()
    .with_ballot_title("Mayor of London")
    .with_post_name("Mayor of London")
    .with_election_name("Mayor of London")
    .with_ballot_paper_id("mayor.london.2024-11-02")
    .with_election_id("mayor.london.2024-11-02")
    .with_voting_system("FPTP")
    .with_candidates(candidates.all_candidates)
)
CANCELLED_BALLOT = BallotBuilder()
REF_BALLOT = BallotBuilder()
AMS_BALLOT = BallotBuilder()
