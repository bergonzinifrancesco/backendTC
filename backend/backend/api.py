from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from .auth.api import router as auth_router
from userInfo.api import router as user_router
from struttura.api import router as struttura_router
from prenotazione.api import router as prenotazione_router
from admin.api import router as admin_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/auth", auth_router)
api.add_router("/user", user_router)
api.add_router("/structure", struttura_router)
api.add_router("/booking", prenotazione_router)
api.add_router("/admin", admin_router)
