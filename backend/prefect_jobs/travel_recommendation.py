from prefect.deployments import run_deployment
from prefect.client.orchestration import get_client


async def get_travel_recommendations(country: str, season: str):

    r = await run_deployment(
        name="recommendations/travel_recommendations_deployment",
        parameters={"country": country, "season": season},
        timeout=0,
    )
    return r.id
