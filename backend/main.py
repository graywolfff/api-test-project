import os
from contextlib import asynccontextmanager

import uvicorn
from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from exceptions.http import NotFoundException
from exceptions.schema import APIError
from models.travel_recommendation import TravelRecommendation
from routes import router_register


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_SERVER')}/?authSource=admin")

    # Initialize beanie with the TravelRecommendation document class
    await init_beanie(
        database=client.recommendation_backend, document_models=[TravelRecommendation]
    )
    # Regis app router
    router_register(app)
    yield
    # Clean up the ML models and release the resources
    client.close()


app = FastAPI(
    lifespan=lifespan,
    title=os.getenv("API_PREFIX", "FAST API"),
    description=os.getenv("API_PREFIX", "api doc"),
    root_path=os.getenv("API_PREFIX", "/api"),
    docs_url="/docs",
    redoc_url="/redoc",
    responses={
        "422": {
            "model": APIError,
            "description": "Validation Error",
        },
        "404": {
            "model": APIError,
            "description": "Not Found",
        },
    },
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Unprocessable Entity",
            "message": "\n".join(error["msg"] for error in exc.errors()),
        },
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": f"{exc.name} not found",
            "message": f"The provided {exc.name} does not exist. Please check the {exc.name} and try again.",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("API_SERVER_PORT", 8000))
    )
