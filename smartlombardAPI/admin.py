from django.contrib import admin
from .models import *


@admin.register(ProductCRM)
class ProductCRMAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    list_filter = ['available', 'category']
