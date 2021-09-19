from django.urls import path
from . import views

urlpatterns = [
    path('import', views.import_js, name='import_js'),  # /specifications/import
]
