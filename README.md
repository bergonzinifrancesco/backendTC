# backendTC
Backend per il progetto di Tecnologie Web.

Il progetto è organizzato in cartelle, non dovrebbe essere necessario conoscere la struttura delle cartelle.


# Istruzioni per l'uso
Dalla cartella base (quella corrente):

```
pipenv shell

cd backend

./manage.py runserver
```

Si aprirà così in http://localhost:8000/api/docs la documentazione dell'API, verificabile tramite OpenApi. È necessario avviare anche il frontend per poter poi visualizzare il sito.

## Software impiegato
Le librerie impiegate sono tutte state scaricate da PyPi, si possono trovare nel Pipfile qui accanto.

## Popola db
Si utilizza il meccanismo delle fixtures per poter caricare dati nel database, qualora fosse vuoto.

Da cartella corrente:

```
cd backend

./manage.py loaddata fixtures/fixtures
```

Si possono visualizzare i dati tramite estensioni per SQLite3.