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