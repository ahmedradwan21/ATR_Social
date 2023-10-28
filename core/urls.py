from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register , name='register'),
    path('login/', views.Login , name='login'),
    path('logout/', views.logout , name='logout'),
    path('settings/', views.settings , name='settings'),
]

