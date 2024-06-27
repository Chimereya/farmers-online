from django import template

register = template.Library()

@register.filter
def sum_prices(order_products):
    return sum(order_product.price for order_product in order_products)
