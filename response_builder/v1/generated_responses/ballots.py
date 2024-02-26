from response_builder.v1.builders.ballots import BallotBuilder, ParlBallotBuilder, StockLocalBallotBuilder  # noqa

LOCAL_BALLOT = StockLocalBallotBuilder()
PARL_BALLOT = ParlBallotBuilder()

GLA_BALLOT = BallotBuilder() 
GLA_C_BALLOT = BallotBuilder()
GLA_A_BALLOT = BallotBuilder()
PR_CL_BALLOT = BallotBuilder()
STV_BALLOT = BallotBuilder()
SV_BALLOT = BallotBuilder()
FPTP_BALLOT = BallotBuilder() 
PCC_BALLOT = BallotBuilder()  
MAYOR_BALLOT = BallotBuilder()  
CANCELLED_BALLOT = BallotBuilder()
REF_BALLOT = BallotBuilder()
AMS_BALLOT = BallotBuilder()

