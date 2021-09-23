from django.urls import path
from . import views

post_list = views.PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = views.PostViewSet.as_view({
    'get': 'retrieve',
    'patch': 'patch',
    'delete': 'destroy'
})

urlpatterns = [
    path('post', post_list, name='post_list'),
    path('post/<int:pk>', post_detail, name='post_detail'),
]