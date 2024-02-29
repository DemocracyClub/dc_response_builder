from response_builder.v1.builders.ballots import (
    StockLocalBallotBuilder, 
)
from response_builder.v1.builders.base import RootBuilder
from response_builder.v1.builders.polling_stations import PollingStationBuilder
from response_builder.v1.models.councils import ElectoralServices
from response_builder.v1.models.polling_stations import (
    Station,
    StationProperties,
)

 
# < -- polling stations -- > 
POLLING_STATION = (
    PollingStationBuilder().set("polling_station_known", True).build()
)
POLLING_STATION.station = Station(id="AA1", type="station", properties=StationProperties(address="Foo Bar"))


# < -- voting systems -- >
FPTP_VOTING_SYSTEM = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_voting_system("FPTP")
STV_VOTING_SYSTEM = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_voting_system("STV")
AMS_VOTING_SYSTEM = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_voting_system("AMS")
SV_VOTING_SYSTEM = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_voting_system("sv")

# < -- election types -- >
LOCAL = StockLocalBallotBuilder().build()
GLA = StockLocalBallotBuilder().with_ballot_title("London Assembly elections").with_post_name("London Assembly").with_election_name("London Assembly elections").with_ballot_paper_id("gla.a.2024-05-02").with_election_id("gla.a.2024-05-02").build()
MAYORAL = StockLocalBallotBuilder().with_ballot_title("Mayor of London").with_post_name("Mayor of London").with_election_name("Mayor of London").with_ballot_paper_id("mayor.london.2024-05-02").with_election_id("mayor.london.2024-05-02").build()
PCC = StockLocalBallotBuilder().with_ballot_title("Police and Crime Commissioner elections").with_post_name("Police and Crime Commissioner for Avon and Somerset").with_election_name("Police and Crime Commissioner election").with_ballot_paper_id("pcc.avon-and-somerset.2024-05-02").with_election_id("pcc.avon-and-somerset.2024-05-02").build()
PARL = StockLocalBallotBuilder().with_ballot_title("Stroud Slade parliamentary by-election").with_post_name("Stroud Slade constituency").with_election_name("Stroud Slade constituency").with_ballot_paper_id("parl.stroud.2024-11-14").with_election_id("parl.stroud.2024-11-14").build()

# < -- root responses -- >
NO_LOCAL_BALLOTS = RootBuilder().without_ballot()

# This is a local ballot by default
CANCELLED_BALLOT = RootBuilder().with_ballot(StockLocalBallotBuilder().build()).with_cancelled()

# LOCAL_BALLOT_WITH_ID_REQUIREMENTS = RootBuilder().with_ballot(StockLocalBallotBuilder().build()).with_id_requirements()

SINGLE_LOCAL_FUTURE_BALLOT_WITH_POLLING_STATION = RootBuilder().with_ballot(StockLocalBallotBuilder().build()).with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="STO",
        name="Stroud Council",
        address="123 Stroud Street",
        email="electoralservices@stroud.gov.uk",
        nation="England",
        phone="123456",
        postcode="GL51AA",
        website="https://stroud.gov.uk"))

SINGLE_LOCAL_FUTURE_BALLOT_WITHOUT_POLLING_STATION = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).without_polling_station().with_electoral_services(
    ElectoralServices(
        council_id="STO",
        name="Stroud Council",
        address="123 Stroud Street",
        email="electoralservices@stroud.gov.uk",
        nation="England",
        phone="123456",
        postcode="GL51AA",
        website="https://stroud.gov.uk"))
    
SINGLE_LOCAL_FUTURE_BALLOT_WITH_ADDRESS_PICKER = RootBuilder().with_ballot(LOCAL).with_address_picker().with_electoral_services(
    ElectoralServices(
        council_id="STO",
        name="Stroud Council",
        address="123 Stroud Street",
        email="",  #
        nation="England",
        phone="123456",
        postcode="GL51AA",
        website="https://stroud.gov.uk"))


MULTIPLE_BALLOTS_WITH_VOTING_SYSTEM_AND_POLLING_STATION = RootBuilder().with_multiple_ballots(
    [MAYORAL, GLA]).with_voting_system("FPTP").with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="WND",
        name="Wandsworth Council",
        address="The Town Hall, Wandsworth High Street",
        email="",  #
        nation="England",
        phone="020 8871 6023",
        postcode="SW118DD",
        website="https://www.wandsworth.gov.uk"))
   
# TO DO: The cancelled ballot is not rendering the expected cancellation 
# message in the template
MULTIPLE_BALLOTS_WITH_CANCELLATION = RootBuilder().with_multiple_ballots(
    [MAYORAL, PARL, GLA, RootBuilder().with_ballot(LOCAL).with_cancelled().build()])

PARL_BALLOT = RootBuilder().with_ballot(
    PARL).with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="STO",
        name="Stroud Council",
        address="123 Stroud Street",
        email="",  #
        nation="England",
        phone="123456",
        postcode="GL51AA",
        website="https://stroud.gov.uk"))
   
GLA_BALLOT = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="WND",
        name="Wandsworth Council",
        address="The Town Hall, Wandsworth High Street",
        email="",  #
        nation="England",
        phone="020 8871 6023",
        postcode="SW118DD",
        website="https://www.wandsworth.gov.uk"))

PCC_BALLOT = RootBuilder().with_ballot(
    PCC).with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="STO",
        name="Stroud Council",
        address="123 Stroud Street",
        email="",  #
        nation="England",
        phone="123456",
        postcode="GL51AA",
        website="https://stroud.gov.uk"))
    
MAYORAL_BALLOT = RootBuilder().with_ballot(
    MAYORAL).with_polling_station(POLLING_STATION).with_electoral_services(
    ElectoralServices(
        council_id="WND",
        name="Wandsworth Council",
        address="The Town Hall, Wandsworth High Street",
        email="",  #
        nation="England",
        phone="020 8871 6023",
        postcode="SW118DD",
        website="https://www.wandsworth.gov.uk"))


  
CANCELLED_BALLOT = RootBuilder().with_ballot(
    StockLocalBallotBuilder().build()).with_electoral_services(
    ElectoralServices(
        council_id="WND",
        name="Wandsworth Council",
        address="The Town Hall, Wandsworth High Street",
        email="",  #
        nation="England",
        phone="020 8871 6023",
        postcode="SW118DD",
        website="https://www.wandsworth.gov.uk")).with_voting_system("FPTP").cancelled(True)
