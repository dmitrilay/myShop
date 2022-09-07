import time
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

from orders.models import OrderItem
from orders.models import Order
from shop.models import Product

from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)


class user_login(LoginView):
    template_name = 'account/login/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('dashboard')


class User_Logout(LogoutView):
    template_name = 'account/logged_out/logged_out.html'


class PasswordReset(PasswordResetView):
    html_email_template_name = 'account/email/password_reset.html'
    template_name = 'account/password_reset/reset_form.html'
    form_class = PasswordResetFormCustom


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset/done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'account/password_reset/confirm.html'
    form_class = SetPasswordFormCustom


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset/complete.html'

# @login_required


def dashboard(request):
    template = 'account/dashboard/dashboard.html'

    UserID = request.user.id

    history_orders = Order.objects.filter(profile=UserID)[:4]

    favorit = FavoriteProduct.objects.filter(profile_favorite=request.user.pk).values('id_product')
    product = Product.objects.filter(pk__in=favorit).prefetch_related('productimage_set').select_related('category')[:3]

    context = {'history_orders': history_orders, 'product': product}

    return render(request, template, context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = f'guest{time.time()}'
            # new_user.username = f'guest{time.time()}'
            # email
            new_user.save()
            Profile.objects.create(user=new_user)

            new_user = authenticate(username=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password'],
                                    )

            login(request, new_user)

            # return render(request, 'account/register_done.html', {'new_user': new_user})
            return render(request, 'account/dashboard/dashboard.html')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserEditPhoneForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')

            return redirect(reverse('dashboard'))
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserEditPhoneForm(instance=request.user.profile)

    template = 'account/changing-data/changing-data.html'
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, template, context)


def history(request):
    """История заказов"""
    if request.user.is_authenticated:
        UserID = request.user.id
    else:
        pass

    pr2 = Order.objects.filter(profile=UserID)
    template = 'account/history-orders/history-orders.html'
    context = {'section': pr2}
    return render(request, template, context)


def history_detail(request, pk):
    if request.user.is_authenticated:
        UserID = request.user.id
    else:
        pass

    pr2 = Order.objects.get(pk=pk)

    template = 'account/order/order.html'
    context = {'section': pr2}
    return render(request, template, context)


def favorite(request):
    form = FavoriteForm(request.POST)
    id_prod = request.POST.get('id_product')
    obj = FavoriteProduct.objects.filter(id_product=id_prod)
    print(obj)
    if obj:
        obj[0].delete()
    else:
        if form.is_valid():
            form.save()

    return HttpResponse(status=201)


def favorites(request):
    favorit = FavoriteProduct.objects.filter(profile_favorite=request.user.pk).values('id_product')
    product = Product.objects.filter(pk__in=favorit).prefetch_related('productimage_set').select_related('category')

    template = 'account/favorites/favorites.html'
    context = {'product': product}
    return render(request, template, context)


def favoritesBoolAjax(request):
    if request.user.is_authenticated:
        pass
    else:
        context = {'total': 'noauth'}
        # return HttpResponse(status=401)
        return JsonResponse(context)

    # product = get_object_or_404(Product, id=product_id)
    # cart.add(product=product)
    favorit = FavoriteProduct.objects.filter(profile_favorite=request.user.pk).values('id_product')
    # print(*list(favorit))
    context = {'total': list(favorit)}
    # print(context)
    # return HttpResponse(status=201)
    return JsonResponse(context)


def favoritesAddAjax(request):
    if request.user.is_authenticated:
        id_prof = request.user.id
        id_prod = request.GET.get('idProduct')
        obj = FavoriteProduct.objects.filter(id_product=id_prod, profile_favorite=id_prof)
        if obj:
            obj[0].delete()
        else:
            prof = Profile.objects.get(pk=id_prof)
            FavoriteProduct.objects.create(id_product=id_prod, profile_favorite=prof, title_product='test')
    return HttpResponse(status=200)
