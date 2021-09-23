from django.urls import path
from . import views

post_list = views.PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('', post_list, name='post_viewset'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('new_post', views.new_post, name='new_post')
]