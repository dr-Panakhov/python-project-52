from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status
from .models import Task

class TaskCrudTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='author', password='password123')
        self.user2 = User.objects.create_user(username='other', password='password123')
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(name='Тест', status=self.status, author=self.user1)

    def test_task_list(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест')

    def test_task_create(self):
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('task_create'), {
            'name': 'Новая задача', 'status': self.status.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())

    def test_task_delete_by_author(self):
        self.client.login(username='author', password='password123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_by_other(self):
        self.client.login(username='other', password='password123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
