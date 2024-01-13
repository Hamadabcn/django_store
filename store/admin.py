from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'amount', 'payment_method', 'items', 'created_at']
    list_per_page = 20
    list_select_related = ['transaction']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def amount(self, obj):
        if obj.transaction:
            return obj.transaction.amount
        return None

    def items(self, obj):
        if obj.transaction and obj.transaction.items:
            return len(obj.transaction.items)
        return None

    def email(self, obj):
        if obj.transaction and obj.transaction.customer_email:
            return obj.transaction.customer_email
        return None

    def payment_method(self, obj):
        if obj.transaction:
            return obj.transaction.get_payment_method_display()
        return None
