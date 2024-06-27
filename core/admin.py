from django.contrib import admin
from .models import (ProductCategory,
                     Product,
                     OrderProduct,
                     Order,
                     Cart,
                     BillingAddress)

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Cart)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'paid', 'billing_address_full_name', 'billing_address_email')

    def billing_address_full_name(self, obj):
        return obj.billing_address.full_name if obj.billing_address else 'N/A'

    def billing_address_email(self, obj):
        return obj.billing_address.email if obj.billing_address else 'N/A'

    billing_address_full_name.short_description = 'Billing Full Name'
    billing_address_email.short_description = 'Billing Email'

admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(OrderProduct)
