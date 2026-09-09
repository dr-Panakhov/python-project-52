from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UsersCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_users_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_user_create(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'Ivan', 
            'last_name': 'Ivanov', 
            'username': 'newuser',
            'password1': 'password123', 
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_update', args=[self.user.id]), {
            'first_name': 'Updated', 
            'last_name': 'Name', 
            'username': 'testuser',
            'password1': 'password123', 
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
