from django.contrib.auth.models import User
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

@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, pk):
    serializer = PostSerializer
    post = Post.objects.filter(pk=pk).first() #이거 별론가?
    if post:
        if (request.method == 'DELETE'):
            post.delete()
            return Response({'message': 'deleted'})
        if (request.method == 'PATCH'):
            post.title = request.data.get('title') if request.data.get('title') is not None else post.title
            post.text = request.data.get('text') if request.data.get('text') is not None else post.text
            post.save()
            post.publish()

        return Response(serializer(post).data)
    else:
        return Response({'message': 'no matching post'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def new_post(request):
    serializer = PostSerializer
    title = request.data.get('title')
    text = request.data.get('text')
    author = request.user if not request.user.is_anonymous else User.objects.get(username='admin') #임시
    created_post = Post.objects.create(title=title, text=text, author=author)
    return Response(serializer(created_post).data, status=status.HTTP_201_CREATED)