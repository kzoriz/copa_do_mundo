from ninja import NinjaAPI
from core.api import router as core_router
from core.auth_api import router as auth_router

api = NinjaAPI(title="API App Copa do Mundo")

api.add_router("/core", core_router)
api.add_router("/auth", auth_router)