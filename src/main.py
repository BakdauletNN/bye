from fastapi import FastAPI
import sys
from pathlib import Path
from src.api.v1.routes.rooms import router as room_r
from src.api.v1.routes.auth import router as auth_r
from core.config import stgs


sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI()
app.include_router(auth_r)
app.include_router(room_r)





