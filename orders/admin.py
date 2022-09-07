from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'email', 'status', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_display_links = ['id', 'first_name', 'email']
    readonly_fields = ['profile']
    inlines = [OrderItemInline]
