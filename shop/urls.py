from django.urls import path
from . import views
from .views import CategoryDetailView2, ProductDetailView

app_name = 'shop'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='StartPageViews'),
    path('category/<str:slug>/', CategoryDetailView2.as_view(), name='product_list_by_category'),
    path('buying/', views.BuyingUp.as_view(), name='buying_up'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    # path('', views.HomeListView.as_view(), name='StartPageViews'),
]
