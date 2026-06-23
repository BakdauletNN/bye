from .auth import router as auth_router
from .rooms import router as rooms_router
from .students import router as students_router
from .applications import router as applications_router
from .checkins import router as checkins_router
from .analytics import router as analytics_router

__all__ = [
    "auth_router",
    "rooms_router",
    "students_router",
    "applications_router",
    "checkins_router",
    "analytics_router",
]
