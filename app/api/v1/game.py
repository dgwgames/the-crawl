from fastapi import APIRouter
from app.core.game_engine import GameEngine

router = APIRouter()
game_engine = GameEngine()

@router.post("/move")
async def move_player(direction: str):
    new_room_description = game_engine.move(direction)
    return {"description": new_room_description}
