from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post

# Create your views here.
@api_view(['GET'])
def post_list(request):
    serializer = PostSerializer
    posts = Post.objects.all()
    return Response(serializer(instance=posts, many=True).data)

@api_view(['GET'])
def post_detail(request, pk):
    serializer = PostSerializer
    post = Post.objects.filter(pk=pk).first() #이거 별론가?
    if post:
        return Response(serializer(post).data)
    else:
        return Response({'message': 'no matching post'}, status=status.HTTP_404_NOT_FOUND)