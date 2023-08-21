from django.urls import path
from django.conf.urls.static import static
from .api import api
from backend.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [path("api/", api.urls)] + static(MEDIA_URL, document_root=MEDIA_ROOT)
