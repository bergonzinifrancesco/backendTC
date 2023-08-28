# backendTC
Backend per il progetto di Tecnologie Web.

Il progetto è organizzato in cartelle, non dovrebbe essere necessario conoscere la struttura delle cartelle.


# Istruzioni per l'uso
Dalla cartella base (quella corrente):

```
sudo docker run --rm -p 6379:6379 redis:7   # necessario per la chat, vedere il tutorial di Django Channels

pipenv shell

cd backend

./manage.py runserver
```

Si aprirà così in http://localhost:8000/api/docs la documentazione dell'API, verificabile tramite OpenApi. È necessario avviare anche il frontend per poter poi visualizzare il sito.

## Software impiegato
Le librerie impiegate sono tutte state scaricate da PyPi, si possono trovare nel Pipfile qui accanto.

## Popola db e fixtures
Si utilizza il meccanismo delle fixtures per poter caricare dati nel database, qualora fosse vuoto.

Da cartella corrente:

```
cd backend

./manage.py loaddata fixtures/fixtures
```

Si possono visualizzare i dati tramite estensioni per SQLite3.

Ho utilizzato questo comando per salvare una copia completa del DB in un file JSON.
```
cd backend
./manage.py dumpdata -a -o fixtures/fixtures.json 
```