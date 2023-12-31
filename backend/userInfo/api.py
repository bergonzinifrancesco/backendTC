from ninja.router import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from userInfo.models import (
    InfoAvanzate,
    PosizioniGioco,
    CaratteristicheGioco,
    AvatarUtente,
)
from ninja import ModelSchema, Schema, UploadedFile, File
from django.core.exceptions import ObjectDoesNotExist
from zxcvbn import zxcvbn
from pydantic.error_wrappers import ValidationError
from userInfo.choices import PosizioniEnum, CaratteristicheEnum
from typing import Optional

router = Router(auth=JWTAuth(), tags=["Utente"])


@router.get("/am_superuser/", response={204: None, 404: None})
def am_superuser(request):
    tmp = User.objects.get(username=request.user)
    if tmp.is_superuser:
        return 204, None
    return 404, None


class Password(Schema):
    password: str


@router.post("/change_password/", response={204: None, 400: str, 409: str, 500: str})
def change_password(request, password: Password):
    """
    Cambio password dell'utente corrente.
    Restituisce: <br>\
        -204 se va tutto bene<br>\
        -400 se la password è debole<br>\
        -409 se la password è uguale alla precedente<br>\
        -500 se non è stato possibile cambiare la password<br>\
    """
    if zxcvbn(password.password)["score"] < 4:
        return 400, "Password più debole della precedente."

    try:
        current_user = User.objects.get(username=request.user)

        if current_user.check_password(password.password):
            return 409, "Password uguale alla precedente."

        current_user.set_password(password.password)

        current_user.save()
        return 204, None

    except Exception as e:
        return 500, e.message


class InfoBase(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "username", "first_name", "last_name", "email"]


@router.get("/me/info_base/", response={200: InfoBase, 404: str})
def get_info_base(request):
    try:
        user = User.objects.get(username=request.user)
        return 200, user
    except Exception as e:
        return 404, str(e)


class PutInfoBase(ModelSchema):
    class Config:
        model = User
        model_fields = ["first_name", "last_name", "email"]


@router.put("/me/info_base/", response={204: None, 400: str})
def put_info_base(request, info: PutInfoBase):
    try:
        tmp = User.objects.get(username=request.user)
        tmp.__dict__.update(info.__dict__)
        tmp.save()
        return 204, None
    except Exception as e:
        # utente non creato
        return 400, str(e)


class Avanzate(ModelSchema):
    class Config:
        model = InfoAvanzate
        model_exclude = ["user_id", "nazionalità", "numero_telefono"]

    nazionalità: str
    numero_telefono: str


@router.get("/me/info_avanzate/", response={200: Avanzate, 404: str})
def get_info_avanzate(request):
    try:
        infoUtente = InfoAvanzate.objects.get(user_id=request.user)
        # workaround per evitare problemi con pydantic
        tmp = infoUtente.__dict__
        # i campi personalizzati sono corretti ma devono essere castati a stringhe
        tmp["nazionalità"] = tmp["nazionalità"].__str__()
        tmp["numero_telefono"] = tmp["numero_telefono"].__str__()
        return 200, tmp
    except Exception as e:
        return 404, str(e)


@router.put("/me/info_avanzate/", response={204: None, 400: str})
def put_info_avanzate(request, info: Avanzate):
    try:
        tmp = InfoAvanzate.objects.get(user_id=request.user)
        tmp.__dict__.update(info.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        try:
            tmp = InfoAvanzate.objects.create(user_id=request.user, **info.dict())
            tmp.save()
            return 204, None
        except Exception as e:
            raise e
    except Exception as e:
        # utente non creato
        return 400, str(e)


@router.get("/me/avatar/", response={200: str, 404: str})
def get_avatar(request):
    try:
        tmp = AvatarUtente.objects.get(img_id=request.user.id)
        return 200, tmp.image
    except Exception as e:
        return 404, str(e)


@router.post("/me/avatar/", response={204: None, 400: str})
def post_avatar(request, file: UploadedFile = File(...)):
    try:
        avatar, _ = AvatarUtente.objects.get_or_create(img_id=request.user)
        avatar.image = file
        avatar.save()
        return 204, None
    except Exception as e:
        return 400, str(e)


class SchemaPosizioni(Schema):
    preferita: PosizioniEnum
    alternativa: Optional[PosizioniEnum]
    alternativa2: Optional[PosizioniEnum]


@router.get("/me/posizioni/", response={200: SchemaPosizioni, 404: str})
def get_posizioni(request):
    try:
        posizioni = PosizioniGioco.objects.get(pos_id=request.user)
        return 200, posizioni
    except Exception as e:
        return 404, str(e)


@router.put("/me/posizioni/", response={204: None, 400: str})
def put_posizioni(request, pos: SchemaPosizioni):
    try:
        tmp = PosizioniGioco.objects.get(pos_id=request.user)
        tmp.__dict__.update(pos.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        try:
            tmp = PosizioniGioco.objects.create(pos_id=request.user, **pos.dict())
            tmp.save()
            return 204, None
        except Exception as e:
            raise e
    except Exception as e:
        # utente non creato
        return 400, str(e)


class SchemaCaratteristiche(Schema):
    principale: CaratteristicheEnum
    secondaria: Optional[CaratteristicheEnum]
    terziaria: Optional[CaratteristicheEnum]


@router.get("/me/caratteristiche/", response={200: SchemaCaratteristiche, 404: str})
def get_caratteristiche(request):
    try:
        caratteristiche = CaratteristicheGioco.objects.get(car_id=request.user)
        return 200, caratteristiche
    except Exception as e:
        return 404, str(e)


@router.put("/me/caratteristiche/", response={204: None, 400: str})
def put_caratteristiche(request, car: SchemaCaratteristiche):
    try:
        tmp = CaratteristicheGioco.objects.get(car_id=request.user)
        tmp.__dict__.update(car.__dict__)
        tmp.save()
        return 204, None
    except ObjectDoesNotExist:
        try:
            tmp = CaratteristicheGioco.objects.create(car_id=request.user, **car.dict())
            tmp.save()
            return 204, None
        except Exception as e:
            raise e
    except Exception as e:
        # utente non creato
        return 400, str(e)
