from re import template
from django.shortcuts import render
from .models import *
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from shop.models import ProductImage


def data_final_cart(obj):
    sum = 0
    for_request = []
    new_array_cart = []
    for i, item in enumerate(obj):
        sum += item['total_price']
        for_request.append(item['product'].name)
        _p = {'product': item['product'].name, 'quantity': item['quantity'], 'total_price': item['total_price']},
        new_array_cart.append(*_p)

    new_array_image = []
    product = ProductImage.objects.filter(product__name__in=for_request)
    for item in product:
        if item.is_main:
            # print()
            new_array_image.append({'image': item.image})

    for i, item in enumerate(new_array_cart):
        new_array_cart[i].update(new_array_image[i])

    return(new_array_cart, sum)


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        total_price = cart.get_total_price()
        if total_price == 0:
            return render(request, 'orders/order/empty.html')

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.profile = request.user.id
            else:
                order.profile = 0
            order.sum_order = total_price
            # order.sum_order = 99999
            # print(order.sum_order)

            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            # запуск асинхронной задачи
            # order_created.delay(order.id)
            order_created(order.id)
            data, sum = data_final_cart(cart)
            template = 'orders/final-order/final-order.html'
            context = {'order': order, 'cart': data, 'sum': sum}
            return render(request, template, context)
    else:
        if request.user.is_authenticated:
            instance = {'first_name': request.user.profile.user.first_name,
                        'email': request.user.profile.user.email,
                        'phone_number': request.user.profile.phone_number,
                        }
            form = OrderCreateForm(instance)
        else:
            form = OrderCreateForm()

    template = 'orders/create/create.html'
    return render(request, template, {'cart': cart, 'form': form})
