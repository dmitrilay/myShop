from django.contrib import admin

from .models import *


class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    """Имя характеристики"""
    list_display = ['name', 'subcategory', 'participation_filtering', 'priority_spec', 'category', ]
    list_editable = ['subcategory', 'participation_filtering', 'priority_spec', ]
    search_fields = ['name']
    list_filter = ['category', 'participation_filtering']
    list_per_page = 30

    raw_id_fields = ['subcategory', ]
    list_select_related = ['category', "subcategory", ]

    def get_queryset(self, request):
        qs = super().get_queryset(self)
        return qs.prefetch_related('category', 'subcategory')


@admin.register(SubcategoriesCharacteristics)
class SubcategoriesCharacteristicsAdmin(admin.ModelAdmin):
    """Категории характеристик"""
    list_display = ['name', 'priority']
    search_fields = ['name']


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    "Характеристика + значение"
    list_display = ['name_product', 'name_spec', 'name_value']
    list_display_links = ['name_product']
    search_fields = ['name_product__name', ]


@admin.register(ValuesSpec)
class ValuesSpecAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(CategoryProducts)
admin.site.register(ProductSpec, ProductSpecAdmin)
