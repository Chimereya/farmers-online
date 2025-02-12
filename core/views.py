from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView,
                                  DetailView,
                                  )
from django.urls import reverse_lazy
from .models import (ProductCategory,
                     Product,
                     OrderProduct,
                     Order,
                     BillingAddress)
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from .forms import CheckoutForm
import requests
import json
from decimal import Decimal
from django.db.models import Sum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist




def home_view(request):
    products = Product.objects.filter(status=1)
    categories = ProductCategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'core/home.html', context)


def product_category(request, category_slug=None):
    product_category = None
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    # if category slug exists, get the slug
    if category_slug:
        product_category = get_object_or_404(ProductCategory, slug=category_slug)
        # filter and display the products by the category
        products = products.filter(product_category=product_category)
    
    context = {
        'category': product_category,
        'categories': categories,
        'products': products
    }
    return render(request, 'core/category.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name='core/detail.html'
    
def get_total_cost(request):
    cart = request.session.get('cart', {})
    total_price = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            new_total_price = product.discount_price * quantity if product.discount_price else product.price * quantity
            total_price += new_total_price
        except ObjectDoesNotExist:
            continue
    
    return JsonResponse({'total_cost': total_price})

def view_cart(request):
    cart = request.session.get('cart', {})
    total_items = 0
    cart_items = []
    total_price = 0
    
    # Check for product existence and update cart accordingly
    updated_cart = {}
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            subtotal = quantity * product.price
            
            # Calculate the amount saved and new total price
            amount_saved = (product.price - product.discount_price) * quantity if product.discount_price else 0
            new_total_price = product.discount_price * quantity if product.discount_price else subtotal
            
            total_price += new_total_price
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal,
                               'amount_saved': amount_saved, 'new_total_price': new_total_price})
            updated_cart[product_id] = item  # Keep the existing item in the updated cart
            total_items += quantity
        except ObjectDoesNotExist:
            # Product no longer exists, so skip it
            pass
    
    # Update session data with the cleaned cart
    request.session['cart'] = updated_cart
    
    return render(request, 'core/cart.html', {'cart_items': cart_items,
                                              'total_price': total_price,
                                              'total_items': total_items})

    
    
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        if str(product_id) not in cart:
            cart[str(product_id)] = {'quantity': 1}
            request.session['cart'] = cart
            total_items = sum(item['quantity'] for item in cart.values())
            return JsonResponse({'success': True, 'message': f"{product.title} added to your cart.", 'total_items': total_items})
        else:
            return JsonResponse({'success': False, 'message': f"{product.title} is already in your cart."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            total_items = sum(item['quantity'] for item in cart.values())
            messages.info(request, f"{product.title} removed from your cart.")
            return redirect('cart')
            # return JsonResponse({'success': True, 'message': f"{product.title} removed from your cart.", 'total_items': total_items})
        else:
            messages.error(request, f"{product.title} is not in your cart.")  
            return redirect('cart')          
            # return JsonResponse({'success': False, 'message': f"{product.title} is not in your cart."})
    else:
        messages.error(request, "Invalid request method")
        return redirect('cart')
        # return JsonResponse({'success': False, 'message': "Invalid request method."})
    
    



def calculate_cart_totals(cart):
    total_items = sum(item['quantity'] for item in cart.values())
    total_cost = sum(
        item['quantity'] * (Product.objects.get(id=pid).discount_price or Product.objects.get(id=pid).price)
        for pid, item in cart.items()
    )
    return total_items, total_cost

def increase_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
            request.session['cart'] = cart
            total_items, total_cost = calculate_cart_totals(cart)
            return JsonResponse({
                'success': True,
                'quantity': cart[str(product_id)]['quantity'],
                'total_items': total_items,
                'total_cost': float(total_cost)
            })
        else:
            return JsonResponse({'success': False, 'message': f"{product.title} is not in your cart."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})

def decrease_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            if cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1
                request.session['cart'] = cart
                total_items, total_cost = calculate_cart_totals(cart)
                return JsonResponse({
                    'success': True,
                    'quantity': cart[str(product_id)]['quantity'],
                    'total_items': total_items,
                    'total_cost': float(total_cost)
                })
            else:
                return JsonResponse({'success': False, 'message': f"Quantity of {product.title} cannot be decreased further."})
        else:
            return JsonResponse({'success': False, 'message': f"{product.title} is not in your cart."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})
    


@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Extract billing address data from the form
            billing_data = {
                'full_name': form.cleaned_data.get('full_name'),
                'email': form.cleaned_data.get('email'),
                'street_address': form.cleaned_data.get('street_address'),
                'apartment_address': form.cleaned_data.get('apartment_address'),
                'zip': form.cleaned_data.get('zip'),
            }

            # Save the billing address
            billing_address = BillingAddress.objects.create(**billing_data)

            # Create order
            order = Order.objects.create(
                user=request.user,
                billing_address=billing_address,
            )

            # Retrieve cart items
            cart = request.session.get('cart', {})
            total_cost = Decimal('0.00')
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                quantity = item['quantity']
                price = product.discount_price if product.discount_price else product.price
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=quantity
                )
                total_cost += price * quantity

            # Save order ID and total cost in session
            request.session['order_id'] = order.id
            request.session['total_cost'] = float(total_cost)
            
            

            # Redirect to payment view
            return redirect('payment_view', order_id=order.id)
    else:
        form = CheckoutForm()

    # Calculate total cost
    total_cost = Decimal('0.00')
    cart = request.session.get('cart', {})
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            total_cost += (product.discount_price if product.discount_price else product.price) * quantity
        except Product.DoesNotExist:
            continue

    context = {
        'form': form,
        'total_cost': float(total_cost),
    }
    return render(request, 'core/payment.html', context)



@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_cost = request.session.get('total_cost', 0)

    context = {
        'order': order,
        'total_cost': total_cost,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'core/payment.html', context)



@csrf_exempt
def verify_transaction(request):
    if request.method == 'POST':
        reference = request.POST.get('reference')
        if not reference:
            return JsonResponse({'status': False, 'message': 'No reference provided'}, status=400)

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data.get('status'):
            try:
                order_id = response_data['data']['metadata']['order_id']
                order = get_object_or_404(Order, id=order_id)
                order.paid = True

                order.save()

                # Clear the cart
                request.session['cart'] = {}

                return JsonResponse({'status': True, 'message': 'Transaction verified successfully'})
            except KeyError:
                return JsonResponse({'status': False, 'message': 'Order ID not found in response'}, status=400)
            except Order.DoesNotExist:
                return JsonResponse({'status': False, 'message': 'Order not found'}, status=404)
        else:
            return JsonResponse({'status': False, 'message': 'Transaction verification failed'}, status=400)

    return JsonResponse({'status': False, 'message': 'Invalid request method'}, status=405)

@login_required
def dashboard_view(request):
    orders = Order.objects.all().select_related('billing_address').prefetch_related('products__product')
    order_products = OrderProduct.objects.all()

    context = {
        'orders': orders,
        'order_products': order_products,
    }
    return render(request, 'core/dashboard.html', context)

def payment_success(request):
    return render(request, 'core/payment_success.html')

