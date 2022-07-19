from django.urls import path
from . import views
# from .views import CategoryDetailView2, ProductDetailView


urlpatterns = [
    path('', views.smartlombardAJAX, name='smartlombardAJAX'),
    # path('search-product-ajax/', views.SearchProductAjax, name='search-product-ajax'),
]
