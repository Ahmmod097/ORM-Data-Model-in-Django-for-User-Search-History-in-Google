from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.userRegister, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('search/', views.saveKeyword, name='search'),
    path('storeKeywords/', views.storedKeyword, name='storedKeyword'),
]