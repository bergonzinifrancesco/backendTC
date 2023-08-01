from ninja.router import Router
from ninja_jwt.authentication import JWTAuth
from struttura.models import AdminStruttura
from django.core.exceptions import ObjectDoesNotExist
from typing import List

router = Router(tags=['Struttura'])

@router.get('/get_structures/', auth=JWTAuth(), response={200: List[int], 404: None})
def am_admin(request):
    '''
        Restituisce l'id di tutte le strutture di cui l'utente attuale è admin.
    '''
    try:
        tmp = AdminStruttura.objects.filter(admin=request.user)
        structures = [i['struttura_id'] for i in tmp.values()]
        return 200, structures
    except ObjectDoesNotExist:
        return 404, None