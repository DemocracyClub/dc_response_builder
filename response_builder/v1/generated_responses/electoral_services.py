from response_builder.v1.models.councils import ElectoralServices

wandsworth_electoral_services = ElectoralServices(
    council_id="WND",
    name="Wandsworth Council",
    address="The Town Hall, Wandsworth High Street",
    email="",  #
    nation="England",
    phone="020 8871 6023",
    postcode="SW118DD",
    website="https://www.wandsworth.gov.uk",
    identifiers=["E09000032"],
)

stroud_electoral_services = ElectoralServices(
    council_id="STO",
    name="Stroud Council",
    address="123 Stroud Street",
    email="",  #
    nation="England",
    phone="123456",
    postcode="GL51AA",
    website="https://stroud.gov.uk",
    identifiers=["E07000082"],
)
