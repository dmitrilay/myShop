import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

from orders.models import OrderItem
from orders.models import Order

from django.contrib.auth.views import LoginView, LogoutView


class user_login(LoginView):
    template_name = 'account/login/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('dashboard')


class User_Logout(LogoutView):
    template_name = 'account/logged_out/logged_out.html'


'''
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
'''


# @login_required
def dashboard(request):
    template = 'account/dashboard/dashboard.html'
    # context = {'section': 'dashboard'}
    return render(request, template)


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
