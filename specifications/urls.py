from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', AllSpecView.as_view(), name='product-list-for-features'),


    path('new-feature/', CreateNewFeature.as_view(), name='new-feature'),
    path('new-validator/', CreateNewFeatureValidator.as_view(), name='new-validator'),
    path('feature-choice/', FeatureChoiceView.as_view(), name='feature-choice-validators'),
    path('feature-create/', CreateFeatureView.as_view(), name='create-feature'),

    path('new-product-feature/', NewProductFeatureView.as_view(), name='new-product-feature'),

    path('search-product/', SearchProductAjaxView.as_view(), name='search-product'),
    path('attach-feature/', AttachNewFeatureToProduct.as_view(), name='attach-feature'),

    path('product-feature/', ProductFeatureChoicesAjaxView.as_view(), name='product-feature'),
    path('attach-new-product-feature/', CreateNewProductFeatureAjaxView.as_view(), name='attach-new-product-feature'),
    path('update-product-features/', UpdateProductFeaturesView.as_view(), name='update-product-features'),
    path('show-product-features-for-update/', ShowProductFeaturesForUpdate.as_view(),
         name='show-product-features-for-update'),

    path('update-product-features-ajax/', UpdateProductFeaturesAjaxView.as_view(), name='update-product-features-ajax'),

    path('import', views.import_js, name='import_js'),  # http://127.0.0.1:8000/specifications/import
    path('priority', views.priority_spec, name='priority_spec'),  # http://127.0.0.1:8000/specifications/priority
    path('delete', views.delete_spec, name='delete_spec'),  # http://127.0.0.1:8000/specifications/delete

    path('editing-subcategory/', views.EditingSubcategory.as_view(), name='editing-subcategory'),
    path('editing-subcategory2/', views.EditingSubcategory2.as_view(), name='editing-subcategory2'),
    path('editing-subcategory-form/', views.forms_subcategories, name='editing-subcategory-form'),
]
