from django.urls import path
from . import views
from .views import CategoryDetailView2, ProductDetailView, SearchListView

app_name = 'shop'

urlpatterns = [
    path('search/', SearchListView.as_view(), name='search-list-view'),
    #
    path('', views.HomeListView.as_view(), name='StartPageViews'),
    # Список товаров
    path('category/<str:slug>/', CategoryDetailView2.as_view(), name='product_list_by_category'),
    #
    path('buying/', views.BuyingUp.as_view(), name='buying_up'),
    # Категории товаров
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    #
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    # path('', views.HomeListView.as_view(), name='StartPageViews'),
    path('product-detail-spec-ajax/', views.ProductDetailSpecAjax, name='product-detail-spec-ajax'),
    #
    path('search-product-ajax/', views.SearchProductAjax, name='search-product-ajax'),
    #
    path('filter-ajax/', views.FilterAjax.as_view(), name='FilterAjax'),
]
