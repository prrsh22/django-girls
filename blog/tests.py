from rest_framework import status

from blog.models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APISimpleTestCase
import datetime

# Create your tests here.
class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create(username="hey")

    def setUp(self):
        self.post = Post.objects.create(author=self.admin, title="title", text="text")

    def test_post가_publish되기전에는_published_date가_null이다(self):
        assert self.post.published_date is None

    def test_post가_publish되면_publish_date가_Null이_아니다(self):
        # given
        self.post.publish()

        # when
        date = self.post.published_date

        # then
        assert abs(date - datetime.datetime.now()) < datetime.timedelta(seconds=10)
    
    def test_post의_Listview는_비어있지않다(self):
        # given
        Post.objects.create(author=self.admin, title="another", text="post")

        # when
        get = self.client.get('')

        # then
        assert get.status_code == status.HTTP_200_OK
        assert len(get.data) == 2
