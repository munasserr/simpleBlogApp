from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Post

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
    
    def test_created_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

class PostTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title="Sample Post", content="Sample Content", author=self.user)
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, "Sample Post")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(Post.objects.count(), 1)

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', email='user@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_registration(self):
        response = self.client.post('/api/register/', {'username': 'newuser', 'password': 'newpassword123', 'password2': 'newpassword123'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue('token' in response.data)

    def test_login(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_create_post_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/blogposts/', {'title': 'Auth Post', 'content': 'Auth content', 'author': self.user.id})
        self.assertEqual(response.status_code, 201)

    def test_create_post_unauthenticated(self):
        response = self.client.post('/blogposts/', {'title': 'Unauth Post', 'content': 'Unauth content'})
        self.assertEqual(response.status_code, 401)