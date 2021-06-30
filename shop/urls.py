from django.urls import path
from . import views
from .views import CategoryDetailView

app_name = 'shop'

urlpatterns = [
    # path('category/telefony/', views.category_p1, name='category_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    path('', views.StartPageViews, name='StartPageViews'),
    path('skupka/', views.skupka, name='SkupkaPageViews'),
    path('product/', views.product_list, name='product_list'),
    path('category/', views.category_list, name='category_list'),
    # path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
