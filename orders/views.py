from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if cart.get_total_price() == 0:
            return render(request, 'orders/order/empty.html')

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.profile = request.user.id
            else:
                order.profile = 0
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            # запуск асинхронной задачи
            order_created.delay(order.id)
            # order_created(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        if request.user.is_authenticated:
            instance = {'first_name': request.user.profile.user.first_name,
                        'email': request.user.profile.user.email,
                        'phone_number': request.user.profile.phone_number,
                        }
            form = OrderCreateForm(instance)
        else:
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
