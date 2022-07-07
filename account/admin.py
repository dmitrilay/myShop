from django.contrib import admin
from .models import *


class FavoriteProductInline(admin.TabularInline):
    model = FavoriteProduct
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number']
    list_display_links = ['id', 'user']
    inlines = [FavoriteProductInline]


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_product', 'id_product']
    list_display_links = ['id', 'title_product']
