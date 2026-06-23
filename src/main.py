from fastapi import FastAPI
from src.api.v1.routes.rooms import router as room_r
from src.api.v1.routes.auth import router as auth_r
from src.api.v1.routes.students import router as students_r
from src.api.v1.routes.applications import router as apps_r
from src.api.v1.routes.checkins import router as checkins_r
from src.api.v1.routes.analytics import router as analytics_r
from src.admin.auth import router as admin_r

app = FastAPI(
    title="Smart Dormitory System",
    description="Dormitory management system",
    version="1.0.0",
)

app.include_router(auth_r)
app.include_router(room_r)
app.include_router(students_r)
app.include_router(apps_r)
app.include_router(checkins_r)
app.include_router(analytics_r)
app.include_router(admin_r)
