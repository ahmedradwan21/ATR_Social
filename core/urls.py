from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register , name='register'),
    path('login/', views.Login , name='login'),
    path('logout/', views.logout , name='logout'),
    path('settings/', views.settings , name='settings'),
    path('post/', views.post , name='Post '),
    path('upload/', views.upload, name='upload'),
    path('like_post/', views.like_post, name='like_post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    re_path(r'^delete_post/(?P<post_id>[0-9a-f-]+)$', views.delete_post, name='delete_post'),
]

