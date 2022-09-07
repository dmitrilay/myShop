from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

p5 = 'password_change/'
p6 = 'password_change/done/'

p7 = 'password_reset/'
p8 = 'password_reset/done/'
p9 = 'reset/<uidb64>/<token>/'
p10 = 'reset/done/'

# app_name = 'account'

urlpatterns = [
    # Авторизация
    path('login/', views.user_login.as_view(), name='login'),
    # path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    #     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.User_Logout.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path(p5, views.ChangePasswordCustom.as_view(), name='password_change'),
    
    path(p6, auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Востановления пароля
    path(p7, views.PasswordReset.as_view(), name='password_reset'),
    path(p8, views.PasswordResetDone.as_view(), name='password_reset_done'),
    path(p9, views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path(p10, views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    # Регистрация пользователя
    path('register/', views.register, name='register'),
    # Изменения профиля
    path('edit/', views.edit, name='edit'),
    path('history/', views.history, name='history'),
    path('history/<int:pk>', views.history_detail, name='history_detail'),
    path('favorite/', views.favorite, name='favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('favoritesBoolAjax/', views.favoritesBoolAjax, name='favoritesBoolAjax'),
    path('favoritesAddAjax/', views.favoritesAddAjax, name='favoritesAddAjax'),
]
