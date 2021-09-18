from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post

# Create your views here.
@api_view(['GET'])
def post_list(request):
    serializer = PostSerializer
    posts = Post.objects.all()
    return Response(serializer(instance=posts, many=True).data)