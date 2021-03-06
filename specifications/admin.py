from django.contrib import admin

from .models import *


class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(SubcategoriesCharacteristics)
class SubcategoriesCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority']
    search_fields = ['name']


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(CategoryProducts)

admin.site.register(ValuesSpec)

admin.site.register(ProductSpec, ProductSpecAdmin)

# admin.site.register(SubcategoriesCharacteristics)
