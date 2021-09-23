from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import PostSerializer
from .models import Post

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        post.publish()
        return super().partial_update(request, *args, **kwargs)