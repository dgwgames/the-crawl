from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.gpt_service import get_gpt_response
from app.db.database import get_singleton_db_connection

router = APIRouter()


# Define a Pydantic model for the request body
class GptRequestBody(BaseModel):
    prompt: str


@router.post("/gpt_interaction")
async def gpt_interaction(request_body: GptRequestBody):
    response = await get_gpt_response(request_body.prompt)
    return {"response": response}
