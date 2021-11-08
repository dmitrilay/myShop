from django.urls import path
from . import views

urlpatterns = [
    path('import', views.import_js, name='import_js'),  # http://127.0.0.1:8000/specifications/import
    path('priority', views.priority_spec, name='priority_spec'),  # http://127.0.0.1:8000/specifications/priority
    path('delete', views.delete_spec, name='delete_spec'),  # http://127.0.0.1:8000/specifications/delete
]
