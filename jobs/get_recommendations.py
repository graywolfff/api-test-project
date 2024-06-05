import os
from typing import TYPE_CHECKING
import asyncio
import prefect
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
from prefect import flow, task

from models.travel_recommendation import TravelRecommendation
from utils.text_cleaner import extract_data

if TYPE_CHECKING:
    from prefect.client.schemas.objects import State

client = OpenAI()
mongo_client = AsyncIOMotorClient(f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_SERVER')}/?authSource=admin")

@task(log_prints=True, cache_result_in_memory=True)
async def get_travel_recommendations(country: str, season: str, /, **kwargs):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"I have traveled to {country}, could you please recommend activities checklist on {season}",
            }
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content


@flow
async def recommendations(country, season):
    state: State = await get_travel_recommendations(country, season, return_state=True)
    await init_beanie(
        database=mongo_client.recommendation_backend, document_models=[TravelRecommendation,]
    )
    data = await state.result(fetch=True)
    activities = extract_data(data)
    
    tonybar = TravelRecommendation(
        uid= prefect.context.get_run_context().flow_run.id,
        country=country,
        season=season,
        recommendations=activities or data,
        status=state.type,
    )

    await tonybar.insert()
    

    
if __name__ == "__main__":
    recommendations.serve(name="travel_recommendations_deployment")
    



