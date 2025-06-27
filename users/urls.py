from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
            path('login/', views.LoginUser.as_view(), name='login_page'),
            path('logout/', views.LogoutUser.as_view(), name='logout_page'),
            path('register/', views.RegisterUser.as_view(), name='register_page'),
            path('activate/<uidb64>/<token>/', views.activate, name='activate'),
            path('confirm-mail/', views.confirm_mail, name='confirm_mail'),
]