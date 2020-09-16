from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

p5 = 'password_change/'
p6 = 'password_change/done/'

p7 = 'password_reset/'
p8 = 'password_reset/done/'
p9 = 'reset/<uidb64>/<token>/'
p10 = 'reset/done/'

urlpatterns = [
    # Авторизация
    #path('login/', views.user_login, name='login'),

    # Авторизация
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # рабочий стол
    path('dashboard', views.dashboard, name='dashboard'),
    # Смена пароля
    path(p5, auth_views.PasswordChangeView.as_view(), name='password_change'),
    path(p6, auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Востановления пароля
    path(p7, auth_views.PasswordResetView.as_view(), name='password_reset'),
    path(p8, auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(p9, auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(p10, auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Регистрация пользователя
    path('register/', views.register, name='register'),
    # Изменения профиля
    path('edit/', views.edit, name='edit'),
]