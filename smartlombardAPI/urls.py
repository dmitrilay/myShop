from django.urls import path
from . import views
# from .views import CategoryDetailView2, ProductDetailView


urlpatterns = [
    path('v1/', views.smartlombardAJAX, name='smartlombardAJAX'),  # http://127.0.0.1:8000/smartlombard/v1/
    path('v2/', views.v2smartlombardAJAX, name='smartlombardAJAX'),  # http://127.0.0.1:8000/smartlombard/v2/
    # path('search-product-ajax/', views.SearchProductAjax, name='search-product-ajax'),
]
