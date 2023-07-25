from ninja.router import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from userInfo.models import InfoAvanzate, PosizioniGioco, CaratteristicheGioco
from ninja import ModelSchema
from django.core.exceptions import ObjectDoesNotExist
from zxcvbn import zxcvbn

router = Router(auth=JWTAuth(), tags=["Utente"])

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


class InfoBase(ModelSchema):
    class Config:
        model = User
        model_fields =  ['id', 'first_name', 'last_name', 'email']

@router.get("/me/info_base/", response={200: InfoBase, 500: str})
def get_info_base(request):
    try:
        user = User.objects.get(username=request.user)
        return 200, user
    except Exception as e:
        return 500, str(e)


class Avanzate(ModelSchema):
    class Config:
        model = InfoAvanzate
        model_exclude = ['user_id']

@router.get("/me/info_avanzate/", response={200: Avanzate, 500: str})
def get_info_avanzate(request):
    try:        
        infoUtente = InfoAvanzate.objects.get(user_id=request.user.id)
        return 200, infoUtente
    except Exception as e:
        return 500, str(e)

@router.put("/me/info_avanzate/", response={204: None, 500: str})
def put_info_avanzate(request, info: Avanzate):
    try:
        tmp = InfoAvanzate.objects.get(user_id=request.user)
        tmp.__dict__.update(info.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        tmp = InfoAvanzate.objects.create(
            user_id=request.user,
            **info.dict()
        )
        tmp.save()
        return 204, None
    except Exception as e:
        # utente non creato
        return 500, str(e)


class Posizioni(ModelSchema):
    class Config:
        model = PosizioniGioco
        model_exclude = ['pos_id']

@router.get("/me/posizioni/", response={200: Posizioni, 500: str})
def get_posizioni(request):
    try:
        posizioni = PosizioniGioco.objects.get(pos_id=request.user.id)
        return 200, posizioni
    except Exception as e:
        return 500, str(e)


@router.put("/me/posizioni/", response={204: None, 500: str})
def put_posizioni(request, pos: Posizioni):
    try:
        tmp = PosizioniGioco.objects.get(pos_id=request.user)
        tmp.__dict__.update(pos.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        tmp = PosizioniGioco.objects.create(
            pos_id=request.user,
            **pos.dict()
        )
        tmp.save()
        return 204, None
    except Exception as e:
        # utente non creato
        return 500, str(e)


class Caratteristiche(ModelSchema):
    class Config:
        model = CaratteristicheGioco
        model_exclude = ['car_id']

@router.get("/me/caratteristiche/", response={200: Caratteristiche, 500: str})
def get_caratteristiche(request):
    try:
        caratteristiche = CaratteristicheGioco.objects.get(car_id=request.user.id)
        return 200, caratteristiche
    except Exception as e:
        return 500, str(e)

@router.put("/me/caratteristiche/", response={204: None, 500: str})
def put_caratteristiche(request, car: Caratteristiche):
    try:
        tmp = CaratteristicheGioco.objects.get(car_id=request.user)
        tmp.__dict__.update(car.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        tmp = CaratteristicheGioco.objects.create(
            car_id=request.user,
            **car.dict()
        )
        tmp.save()
        return 204, None
    except Exception as e:
        # utente non creato
        return 500, str(e)