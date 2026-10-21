from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('contract', 'item', 'client', 'branch', 'service', 'receive_date', 'get_cost', 'get_excerpt')


admin.site.register(Order, OrderAdmin)
