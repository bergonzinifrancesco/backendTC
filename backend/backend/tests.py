from django.test import TestCase, Client
from struttura.models import Struttura
from struttura.api import get_structure_info


# Create your tests here.
class TestStruttura(TestCase):
    def setUp(self):
        Struttura.objects.create(nome="Pippo Paperino")

    def test_if_structure_has_info(self):
        s = Struttura.objects.get(nome="Pippo Paperino")
        self.assertEqual(get_structure_info(self, 1), (200, s))

    def test_if_structure_is_not_there(self):
        Struttura.objects.get(nome="Pippo Paperino").delete()
        self.assertEqual(
            get_structure_info(self, 1), (404, "La struttura selezionata non esiste.")
        )

    def tearDown(self):
        Struttura.objects.all().delete()


c = Client()
response = c.post(
    "/api/token/pair",
    {"password": "ciaomichiamopaperino", "username": "nicolo"},
    content_type="application/json",
)

print("\n", response, "\n")

if response.status_code != 200:
    print("Non esiste l'utente nicolo\n")
else:
    print("Utente nicolo trovato\n")
