from ninja.router import Router
from ninja_jwt.authentication import JWTAuth
from typing import List, Dict, Tuple
from typing_extensions import TypedDict
from django.contrib.auth.models import User
from ninja import Schema, ModelSchema
from struttura.models import AdminStruttura, Struttura
from django.core.exceptions import ObjectDoesNotExist

router = Router(tags=["Admin"])


@router.get(
    "/list_users_by_username_and_id/",
    response={200: List[Tuple[str, int]], 403: str, 500: str},
    auth=JWTAuth(),
)
def get_users_by_username(request):
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"
    try:
        users = User.objects.values_list("username", "id")
        users = users.exclude(username=request.user)
        return 200, users
    except Exception as e:
        return 500, str(e)


@router.get(
    "/{id_struttura}/get_usernames_of_admins/",
    response={200: List[str], 403: None, 404: str, 500: str},
    auth=JWTAuth(),
)
def get_usernames_of_admins(request, id_struttura: int):
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"

    try:
        try:
            struttura = Struttura.objects.get(id=id_struttura)
            admins = AdminStruttura.objects.filter(struttura=struttura).values_list(
                "admin", flat=True
            )
            return 200, [str(User.objects.get(id=u)) for u in admins]
        except ObjectDoesNotExist:
            return 404, "Struttura non trovata"
        except Exception as e:
            raise e
    except Exception as e:
        return 500, str(e)


@router.get(
    "/get_admins_of_structures/",
    response={200: Dict[int, List[str]], 403: str, 404: str},
    auth=JWTAuth(),
)
def get_admins_of_structures(request):
    """
    Si restituisce un dizionario di tipo {struttura: [admins]}
    """
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"

    couples = {}
    try:
        assignments = AdminStruttura.objects.values("admin", "struttura")
        for assignment in assignments:
            admin = str(User.objects.get(id=assignment["admin"]))
            structure = assignment["struttura"]

            if admin not in couples:
                couples[structure] = [admin]
            else:
                couples[structure] += [admin]

        return 200, couples
    except Exception as e:
        return 404, str(e)


class Assignment(TypedDict):
    user: int
    structure: int


@router.post(
    "/assign_users_to_structures/",
    response={204: None, 403: str, 500: str},
    auth=JWTAuth(),
)
def assign_users_to_structures(request, assignments: List[Assignment]):
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"

    try:
        for assignment in assignments:
            admin = User.objects.get(id=assignment["user"])
            struttura = Struttura.objects.get(id=assignment["structure"])
            AdminStruttura.objects.update_or_create(admin=admin, struttura=struttura)
        return 204, None
    except Exception as e:
        return 500, str(e)


@router.post(
    "/remove_users_to_structures/",
    response={204: None, 403: str, 500: str},
    auth=JWTAuth(),
)
def remove_users_from_structures(request, assignments: List[Assignment]):
    """
    La lista di accoppiamenti utente-struttura da cancellare (se l'utente è admin)
    """
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"

    try:
        for assignment in assignments:
            admin = User.objects.get(id=assignment["user"])
            struttura = Struttura.objects.get(id=assignment["structure"])
            AdminStruttura.objects.get(admin=admin, struttura=struttura).delete()
        return 204, None
    except Exception as e:
        return 500, str(e)


@router.delete(
    "/remove_structure/",
    response={200: str, 403: str, 404: str, 500: str},
    auth=JWTAuth(),
)
def remove_structure_by_id(request, id_struttura: int):
    if not request.user.is_superuser:
        return 403, "Non sei admin del sito"

    try:
        s = Struttura.objects.get(id=id_struttura)
        s.delete()
        return 200, "Rimozione della struttura avvenuta con successo."
    except ObjectDoesNotExist:
        return 404, "Struttura non trovata"
