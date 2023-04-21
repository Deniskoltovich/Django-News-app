from django.urls import path, include
from accounts.views import register, logout_user

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('', include('django.contrib.auth.urls')),

]