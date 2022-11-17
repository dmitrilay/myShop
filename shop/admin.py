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


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    exclude = ('imageOLD', 'name', 'compression')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_spec', 'price', 'available', 'sold', 'created', 'updated')
    list_filter = ('condition', 'category', 'available', 'sold',)
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    # fields = ['name', 'slug', 'price', 'category', 'features', 'productimage.image']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'compression', 'product', 'get_html_img')
    list_display_links = ('id', 'name', 'product')
    fields = ('product', 'image', 'imageOLD', 'name', 'is_main', 'compression')
    readonly_fields = ('is_main',  'imageOLD', 'compression')

    list_per_page = 100

    def get_html_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=60>")

    get_html_img.short_description = 'Изображение'
