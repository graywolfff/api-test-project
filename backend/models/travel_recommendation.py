from beanie import Document, init_beanie, Indexed
from uuid import uuid4, UUID
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from typing import Annotated
import os

class TravelRecommendation(Document):
    uid: Annotated[UUID, Indexed(unique=True)]
    country: str
    season: str
    recommendations: list[str] = []
    status: str

    class Settings:
        name = "travel_recommendation_collection"
