from ninja.router import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from zxcvbn import zxcvbn

router = Router(auth=JWTAuth())

@router.patch('/change_password', response={204: None, 400: str, 409: str, 500: str})
def change_password(request, password: str):
    '''
    Cambio password dell'utente corrente.
    Restituisce: <br>\
        -204 se va tutto bene<br>\
        -400 se la password è debole<br>\
        -409 se la password è uguale alla precedente<br>\
        -500 se non è stato possibile cambiare la password<br>\
    '''
    if(zxcvbn(password)['score'] < 4):
        return 400, "Password più debole della precedente."

    try:
        current_user = User.objects.get(username=request.user)
        
        if(current_user.check_password(password)):
            return 400, "Password uguale alla precedente."
        
        current_user.set_password(password)
        
        current_user.save()
        return 204, None

    except Exception as e:
        return 500, e.message

from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields =  ['id', 'first_name', 'last_name', 'email']

@router.get("/me", response={200: UserSchema, 500: str})
def get_info(request):
    try:
        user = User.objects.get(username=request.user)
        return 200, user
    except Exception as e:
        return 500, str(e)