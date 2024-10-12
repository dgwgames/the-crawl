from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.models import PlayerModel
from app.core.game_engine import GameEngine
from app.db.database import get_connection
import logging

router = APIRouter()
game_engine = GameEngine()

logging.basicConfig(level=logging.DEBUG)  # Set up logging


class PlayerRegistration(BaseModel):
    name: str


class PlayerMove(BaseModel):
    player_name: str
    direction: str


@router.post("/register")
async def register_player(player: PlayerRegistration, connection=Depends(get_connection)):
    PlayerModel.create_player(connection, name=player.name)
    return {"message": f"Player '{player.name}' has been registered."}


@router.post("/move")
async def move_player(move: PlayerMove, connection=Depends(get_connection)):
    logging.debug(f"Attempting to move player: {move.player_name} in direction: {move.direction}")

    player = PlayerModel.get_player_by_name(connection, move.player_name)
    if not player:
        logging.error(f"Player '{move.player_name}' not found.")
        raise HTTPException(status_code=400, detail=f"Player '{move.player_name}' not found.")

    result = game_engine.move(connection, move.player_name, move.direction)

    if result["success"]:
        logging.debug(f"Player '{move.player_name}' moved successfully: {result['message']}")
        return {"message": result["message"]}
    else:
        logging.error(f"Failed to move player '{move.player_name}': {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])
