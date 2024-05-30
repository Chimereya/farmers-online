from django.contrib import admin
from .models import (ProductCategory,
                     Product,
                     OrderProduct,
                     Order,
                     Cart,
                     BillingAddress)

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(BillingAddress)