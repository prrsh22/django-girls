from blog.models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APISimpleTestCase
import datetime

# Create your tests here.
class PostTest(TestCase):
    def test_post_publish(self):
        admin = User.objects.create(username="hey")
        post = Post.objects.create(author=admin, title="", text="")
        assert post.published_date is None
        post.publish()
        assert post.published_date < datetime.datetime.now()
    
    def test_post_list(self):
        posts = Post.objects.all()
        post_list_res = self.client.get('')
        assert len(post_list_res.data) == len(posts)

    def test_new_post(self):
        #given
        user = User.objects.create(username='test')
        self.client.force_login(user=user)
        post_number_before_create = len(Post.objects.all())

        #when
        created_post = self.client.post('/new_post', {'title': '', 'text': ''})

        #then
        post_number_after_create = len(Post.objects.all())
        assert created_post.status_code == 201
        assert post_number_after_create == post_number_before_create + 1
    
    def test_GET_not_existing_post_return_404(self):
        #given
        number_of_posts = len(Post.objects.all())

        #when
        response = self.client.get(f'/post/{number_of_posts+1}')

        #then
        assert response.status_code == 404
    
    def test_GET_existing_post_return_200(self):
        #given
        author = User.objects.create(username="hey")
        post = Post.objects.create(author=author, title="", text="")

        #when
        response = self.client.get(f'/post/{post.id}')

        #then
        assert response.status_code == 200