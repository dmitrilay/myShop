from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from cart.forms import CartAddProductForm


# @require_POST  # Декоратор позволяет представлению обрабатывать только POST-запросы.
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_add_js(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    context = {'total': len(cart)}
    # return HttpResponse(status=201)
    return JsonResponse(context)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/cart/cart.html', {'cart': cart})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    tempates = 'shop/product/detail.html'
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, tempates, context)


def ChangeItemAjax(request):
    product_id = request.GET.get('product_id')
    change = request.GET.get('item')
    cart = Cart(request)

    if change == 'add':
        cart.changeAdd(product_id)
    elif change == 'reduce':
        cart.changeReduce(product_id)

    total_price = cart.get_total_price()
    total_price_item = cart.get_total_price_item(product_id)
    cart_item = len(cart)

    context = {'total_price': total_price, 'total_price_item': total_price_item, 'cart_item': cart_item}
    # print(request.GET.get('product_id'))
    # return HttpResponse(status=200)
    return JsonResponse(context)
