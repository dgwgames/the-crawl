from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.database import get_db_connection
from app.db.models import PlayerModel
from app.core.game_engine import GameEngine

router = APIRouter()
game_engine = GameEngine()


class PlayerRegistration(BaseModel):
    name: str


class PlayerMove(BaseModel):
    player_name: str
    direction: str


@router.post("/register")
async def register_player(player: PlayerRegistration):
    connection = get_db_connection()
    PlayerModel.create_player(connection, name=player.name)
    return {"message": f"Player '{player.name}' has been registered."}


@router.post("/move")
async def move_player(move: PlayerMove):
    connection = get_db_connection()
    result = game_engine.move(connection, move.player_name, move.direction)
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=400, detail=result["message"])
