from django.contrib import admin
from .models import *


@admin.register(ProductCRM)
class ProductCRMAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['available', 'category']


class ProductCRMImageInline(admin.TabularInline):
    model = NewProductCrmImage
    extra = 0


@admin.register(NewProductCRM)
class NewProductCRMAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['available', 'category']
    exclude = ['slug', 'condition']
    readonly_fields = ['article']
    inlines = [ProductCRMImageInline]


admin.site.register(NewProductCrmImage)
