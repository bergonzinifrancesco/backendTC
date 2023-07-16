from ninja.router import Router
from django.contrib.auth.models import User
from ninja import Schema
from typing import List
from zxcvbn import zxcvbn
from email_validator import validate_email, EmailNotValidError
from ninja_jwt.tokens import RefreshToken

router = Router()

class SignupUser(Schema):
    username:str
    password:str
    first_name:str
    last_name:str
    email:str

class UserToken(Schema):
    refresh: str
    access: str

class PasswordFeedback(Schema):
    score: int = 0
    warnings:str|List[str] = None
    suggestions:str|List[str] = None

class ConflictError(Schema):
    username:str = None
    email:str = None
    message:str = None

@router.post('register/', tags=['Django Ninja Auth'], response={200: UserToken, 400: PasswordFeedback, 409: ConflictError, 500: str})
def register_user(request, user: SignupUser):
    '''
        Funzione di registrazione utenti. Restituisce i token JWT se va a buon fine.

        Errori:
            - 400 se la password è debole
            - 409 se ci sono problemi con username od email
            - 500 se il server non riesce a creare l'utente
    '''

    # utente già presente, early exit con Conflict Error
    if(User.objects.get(username=user.username)):
        return 409, {
            'username': user.username,
            'message': "Username già presente."
        }
    
    # controllo email e normalizzazione della stessa, no resolver DNS
    try:
        normalized_email = validate_email(user.email, check_deliverability=False)
        user.email = normalized_email
    except EmailNotValidError:
        return 409, {
            'email': user.email,
            'message': "Email non valida, formato errato."
        }

    # uso di zxcvbn per valutare la bontà della password
    password_evaluation = zxcvbn(user.password)

    feedback = password_evaluation['feedback']
    
    warnings = feedback['warning']
    suggestions = feedback['suggestions']

    # se c'è feedback, la password è migliorabile
    if(warnings or suggestions):
        return 400, {
            'score': password_evaluation['score'],
            'warnings': warnings,
            'suggestions':suggestions
        }

    # creazione utente nel db e salvataggio
    new_user = User.objects.create_user(**user.dict())
    if new_user:
        new_user.save()
        # generazione token e restituzione
        jwt_token = RefreshToken.for_user(new_user)
        if jwt_token:
            return 200, {
                'refresh': str(jwt_token),
                'access': str(jwt_token.access_token)
            }

    # return di default, corrisponde ad errore nella creazione dell'utente
    return 500, {'message': "Errore nella registrazione dell'utente"}
