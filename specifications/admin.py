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


@admin.register(SubcategoriesCharacteristics)
class SubcategoriesCharacteristicsAdmin(admin.ModelAdmin):
    """Категории характеристик"""
    list_display = ['name', 'priority']
    search_fields = ['name']


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    "Характеристика + значение"
    list_display = ['name_product']
    search_fields = ['name', ]


@admin.register(ValuesSpec)
class ValuesSpecAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(CategoryProducts)
admin.site.register(ProductSpec, ProductSpecAdmin)
