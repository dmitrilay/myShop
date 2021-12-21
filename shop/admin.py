from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created', 'updated']
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    # fields = ['name', 'slug', 'price', 'category', 'features', 'productimage.image']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_html_img']
    list_display_links = ['id', 'product']
    fields = ['product', 'image', 'name', 'is_main', 'is_active', 'created', 'updated']
    readonly_fields = ('is_main', 'is_active', 'created', 'updated')

    def get_html_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=60>")

    get_html_img.short_description = 'Изображение'
