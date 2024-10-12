from fastapi import FastAPI
from app.api.v1 import player

app = FastAPI(title="Dungeon Crawler Backend")

# Include our different routers for organizing endpoints
app.include_router(player.router, prefix="/api/v1/player", tags=["Player"])
