from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status

class StatusCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.status = Status.objects.create(name='Новый')

    def test_status_list_unauthorized(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_status_list_authorized(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')

    def test_status_create(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('status_create'), {'name': 'В работе'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('status_update', args=[self.status.id]), {'name': 'Завершен'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Завершен')

    def test_status_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
