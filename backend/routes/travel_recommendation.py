from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from prefect import exceptions
from prefect.client.orchestration import get_client
from prefect.client.schemas.objects import StateType

from exceptions.http import NotFoundException
from models.travel_recommendation import TravelRecommendation
from prefect_jobs.travel_recommendation import get_travel_recommendations
from schemas.objects import EntityIndex, Season
from schemas.objects import TravelRecommendation as TravelRecommendationTDO
from schemas.objects import TravelRecommendationBase as TravelRecommendationBaseTDO

recommendation_router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@recommendation_router.get("/")
async def request_recommendations(country: str, season: Season) -> EntityIndex:
    # Triger backgound job and return job id immediately.
    flow_id = await get_travel_recommendations(country, season)
    return {"uid": flow_id}


@recommendation_router.get("/{recommendation_id}")
async def get_recommendations_by_id(
    recommendation_id: UUID,
) -> Union[
    TravelRecommendationTDO,
    TravelRecommendationBaseTDO,
]:
    # check the prefect flow first incase user reqest have done yet.
    client = get_client()
    try:
        flow_run = await client.read_flow_run(str(recommendation_id))
    except exceptions.ObjectNotFound:
        raise NotFoundException(
            name="UID",
        )
    if flow_run.state_type != StateType.COMPLETED:
        return JSONResponse(
            status_code=200,
            content={
                "uid": str(flow_run.id),
                "status": flow_run.state_name,
                "message": "The recommendations are not yet available. Please try again later.",
            },
        )

    data = await TravelRecommendation.find_one({"uid": recommendation_id})
    return data.model_dump(exclude=["id"])
