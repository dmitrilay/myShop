from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product
from .models import *


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    readonly_fields = ['imageOLD']
    list_display_links = ['id', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    exclude = ['imageOLD', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_spec', 'price', 'available', 'sold', 'created', 'updated']
    list_filter = ['category', 'available', 'sold', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    # fields = ['name', 'slug', 'price', 'category', 'features', 'productimage.image']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_html_img']
    list_display_links = ['id', 'product']
    fields = ['product', 'image', 'imageOLD', 'name', 'is_main', 'is_active', 'created', 'updated']
    readonly_fields = ('is_main', 'is_active', 'created', 'updated', 'imageOLD')

    list_per_page = 10

    def get_html_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=60>")

    get_html_img.short_description = 'Изображение'
