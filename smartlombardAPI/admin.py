from django.contrib import admin
from .models import *


class OldProductCRMImageInline(admin.TabularInline):
    model = OldProductCrmImage
    extra = 0


@admin.register(ProductCRM)
class ProductCRMAdmin(admin.ModelAdmin):
    list_display = ['name', 'sold']
    list_filter = ['available', 'category', 'sold']
    readonly_fields = ['article']
    exclude = ['slug']
    inlines = [OldProductCRMImageInline]

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        # extra_context['show_save'] = False
        return super(ProductCRMAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


class ProductCRMImageInline(admin.TabularInline):
    model = NewProductCrmImage
    extra = 0


@admin.action(description='Удаление публикаций прошедших модерацию')
def make_published(modeladmin, request, queryset):
    """Удаление данных которые уже прошли модерацию"""
    queryset.filter(available=True).delete()


@admin.register(NewProductCRM)
class NewProductCRMAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'storage', 'category', 'price']
    list_filter = ['available', 'category']
    exclude = ['slug', 'condition']
    readonly_fields = ['article']
    inlines = [ProductCRMImageInline]
    actions = [make_published]


admin.site.register(NewProductCrmImage)
admin.site.register(OldProductCrmImage)
