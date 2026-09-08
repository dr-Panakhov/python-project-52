from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Label

class LabelCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.label = Label.objects.create(name='bug')

    def test_label_list(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bug')

    def test_label_create(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('label_create'), {'name': 'feature'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='feature').exists())

    def test_label_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
