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
    path('notifications/', views.notification, name='notifications'),
    # path('update_username/', views.update_username, name='update_username'),
    re_path(r'^delete_post/(?P<post_id>[0-9a-f-]+)$', views.delete_post, name='delete_post'),
    # re_path(r'^edit_post/(?P<post_id>[0-9a-f-]+)$', views.delete_post, name='edit'),
    path('edit_post/<uuid:post_id>/', views.edit_post, name='edit_post'),
    path('view_post/<uuid:post_id>/', views.view_post, name='view_post'),
    path('view_post/<uuid:post_id>/', views.view_post, name='view_post'),
    path('add_comment/<uuid:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]

