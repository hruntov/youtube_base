from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile
from youtubers.models import Youtuber


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration(self):
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('sign_up'), registration_data)
        self.assertEqual(response.status_code, 200)

        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_logout(self):
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)
        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('login'),
                                    {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)


class LogoutTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_logout(self):
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertNotIn('_auth_user_id', self.client.session)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.youtuber = Youtuber.objects.create(username='testyoutuber', slug_name='testyoutuber')
        self.client.login(username='testuser', password='testpassword')

    def test_subscription(self):
        response = self.client.post(reverse('manage_subscribe', args=[self.youtuber.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.youtuber in self.user.profile.subscriptions.all())

    def test_unsubscription(self):
        self.user.profile.subscriptions.add(self.youtuber)
        response = self.client.post(reverse('manage_subscribe', args=[self.youtuber.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.youtuber in self.user.profile.subscriptions.all())
