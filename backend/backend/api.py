from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from .auth.api import router as auth_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router('/auth', auth_router)
