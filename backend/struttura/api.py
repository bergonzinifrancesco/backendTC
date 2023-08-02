from ninja.router import Router
from ninja import ModelSchema
from ninja_jwt.authentication import JWTAuth
from struttura.models import AdminStruttura, Struttura
from django.core.exceptions import ObjectDoesNotExist
from typing import List

router = Router(tags=['Struttura'])

@router.get('/my_structures/', auth=JWTAuth(), response={200: List[int], 404: None})
def am_admin(request):
    '''
        Restituisce l'id di tutte le strutture di cui l'utente attuale è admin.
    '''
    try:
        tmp = AdminStruttura.objects.filter(admin=request.user)
        structures = [i['struttura_id'] for i in tmp.values()]

        # se la lista non è vuota
        if structures:
            return 200, structures
        return 404, None
    except ObjectDoesNotExist:
        return 404, None


class SchemaStruttura(ModelSchema):
    class Config:
        model = Struttura
        model_exclude = ['id']

@router.get('/{id}/info/', response={200: SchemaStruttura, 404: str})
def get_structure_info(request, id:int):
    try:
        tmp = Struttura.objects.get(id=id)
        return 200, tmp
    except ObjectDoesNotExist:
        return 404, "La struttura selezionata non esiste."


@router.get('/list_structures/', response={200: List[int], 404: str})
def list_structures(request):
    '''
        Restituisce tutti gli id delle strutture presenti.
    '''
    try:
        tmp = Struttura.objects.all()
        return 200, [e.id for e in tmp]
    except ObjectDoesNotExist:
        return 404, "Non ci sono strutture memorizzate."