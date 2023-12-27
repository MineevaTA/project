from django.contrib.auth import get_user_model
from django.test import TestCase
import sys
sys.path.append(".")

from ..models import Post

User = get_user_model()

class PostTest(TestCase):
    def setUp(self):
        self.author_1 = User.objects.create(username='author #1')
        self.author_2 = User.objects.create(username='author #2')
        Post.objects.create(title='Blog Post #1', text='Dummy text #1', author=self.author_1)
        Post.objects.create(title='Blog Post #2', text='Dummy text #2', author=self.author_2)

    def test_publish_method_for_post(self):
        post = Post.objects.get(title='Blog Post #1')
        post.publish()
        self.assertEqual(post.is_published, True)
