from typing import TYPE_CHECKING
from .travel_recommendation import recommendation_router

if TYPE_CHECKING:
    from fastapi import FastAPI


def router_register(app: "FastAPI"):
    app.include_router(recommendation_router, prefix="/v1")
