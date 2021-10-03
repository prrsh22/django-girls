from rest_framework import status
from blog.models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APISimpleTestCase
import datetime
from pytest_postgresql import factories

# Create your tests here.
class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create(username="test")

    def setUp(self):
        self.post = Post.objects.create(author=self.testuser, title="title", text="text", category="cat")

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
        Post.objects.create(author=self.testuser, title="another", text="post")

        # when
        get = self.client.get('/post/')

        # then
        assert get.status_code == status.HTTP_200_OK
        assert len(get.data) == 2

    def test_post가_생성되면_201을_반환한다(self):
        #given
        self.client.force_login(user=self.testuser)

        #when
        created_post = self.client.post('/post/', {'title': 'test title', 'text': 'test text', 'author': self.testuser.id})

        #then
        assert created_post.status_code == 201

    def test_post가_생성되면_글_수가_늘어난다(self):
        #given
        self.client.force_login(user=self.testuser)
        post_number_before_create = Post.objects.count()

        #when
        created_post = self.client.post('/post/', {'title': 'test2', 'text': 'test2 text', 'author': self.testuser.id})

        #then
        post_number_after_create = Post.objects.count()
        assert post_number_after_create == post_number_before_create + 1
    
    def test_없는_post를_조회하면_404를_반환한다(self):
        #given
        number_of_posts = len(Post.objects.all())

        #when
        get = self.client.get(f'/post/{number_of_posts+1}/')

        #then
        assert get.status_code == 404
    
    def test_있는_post를_조회하면_200을_반환한다(self):
        #when
        get = self.client.get(f'/post/{self.post.id}/')

        #then
        assert get.status_code == 200

    def test_post를_patch하면_수정된다(self):
        #when
        self.client.patch(f'/post/{self.post.id}/', {"title": "updated title", "text": "updated text"}, content_type='application/json')

        #then
        updated_post = Post.objects.get(id=self.post.id)
        assert updated_post.title == 'updated title'
        assert updated_post.text == 'updated text'
    
    def test_post를_delete하면_글_수가_줄어든다(self):
        #given
        number_of_posts_before_delete = Post.objects.count()

        #when
        self.client.delete(f'/post/{self.post.id}/')

        #then
        number_of_posts_after_delete = Post.objects.count()
        assert number_of_posts_after_delete == number_of_posts_before_delete - 1

    def test_category가_주어지면_title_앞에_붙지_않고_따로_저장된다(self):
        #when
        self.client.post('/post/', {"category": "야구", "title": "치킨치킨치킨", "text": "yeah", 'author': self.testuser.id})
        
        #then
        assert Post.objects.last().category == "야구"
        assert Post.objects.last().title != "[야구] 치킨치킨치킨"

    def test_category는_GET에서_제외된다(self):
        #when
        get = self.client.get(f'/post/{self.post.id}/')

        #then
        assert "category" not in get.data
    
    def test_post_조회시_title_with_category_가_반환된다(self):
        #when
        get = self.client.get(f'/post/{self.post.id}/')

        #then
        assert get.data["title_with_category"] == "[cat] title"
    
    def test_title은_5자_이상이어야_한다(self):
        #when
        post = self.client.post('/post/', {"category": "야구", "title": "치킨", "text": "yeah", 'author': self.testuser.id})

        #then
        assert post.status_code == status.HTTP_400_BAD_REQUEST

    def test_title에_야구가_있으면_category는_야구여야_한다(self):
        #when
        post = self.client.post('/post/', {"category": "치킨", "title": "야구장 가고 싶다", "text": "yeah", 'author': self.testuser.id})

        #then
        assert post.status_code == status.HTTP_400_BAD_REQUEST