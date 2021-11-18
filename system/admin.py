from django.contrib import admin
from django.db import models
from system.models import Customers, Item, Purchases, Sales, SellingPrice, Suppliers
from system.models import Account

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ItemAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'category', 'color', 'description']

    list_filter = ['product_code', 'category']
    search_fields = ['product_code', 'category']

class SellingAdmin(admin.ModelAdmin):
    list_display = ['item', 'selling_price']

admin.site.register(Item)
admin.site.register(SellingPrice)
admin.site.register(Suppliers)
admin.site.register(Purchases)
admin.site.register(Customers)
admin.site.register(Sales)


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

