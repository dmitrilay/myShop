from django.urls import path
from .views import photo_replacement_api_viev


app_name = 'shop_api'

urlpatterns = [
    path('photo/v1', photo_replacement_api_viev.as_view(), name='photo_replacement_api'),
]
