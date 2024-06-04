
def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    return {'total_items': total_items}
