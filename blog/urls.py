from django.conf.urls import url
from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'post', views.PostViewSet, basename="post")

urlpatterns = router.urls