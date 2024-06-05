from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from typing import List
from prefect.client.schemas.objects import StateType


class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class EntityIndex(BaseModel):
    uid: UUID


class TravelRecommendationBase(EntityIndex):
    status: StateType


class TravelRecommendation(TravelRecommendationBase):
    country: str
    season: str
    recommendations: List[str]
