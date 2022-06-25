from django.contrib import admin

from .models import *


class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(CategoryProducts)
admin.site.register(Specifications)
admin.site.register(ValuesSpec)
admin.site.register(CharacteristicValue)
admin.site.register(ProductSpec, ProductSpecAdmin)
