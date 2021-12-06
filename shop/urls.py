from django.urls import path
from . import views
from .views import CategoryDetailView, CategoryDetailView2
from .views import ProductDetailView

app_name = 'shop'

urlpatterns = [
    path('category/<str:slug>/', CategoryDetailView2.as_view(), name='product_list_by_category'),
    path('', views.HomeListView.as_view(), name='StartPageViews'),
    path('buying/', views.BuyingUp.as_view(), name='buying_up'),
    path('', views.HomeListView.as_view(), name='StartPageViews'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='product_list_by_category'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),

    # path('product/', views.product_list, name='product_list'),
    # path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]
