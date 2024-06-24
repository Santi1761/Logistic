from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from logistic.models import Event
from logistic.models import Task

class TestTask(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.event = Event.objects.create(name='Test Event', executionDate=timezone.now() + timedelta(days=7), place='Test Place', progress=0, user=self.user)
        self.task = Task.objects.create(name='Test Task', event=self.event, user=self.user)

    def test_create_task_view(self):
        """ Test for: creating a task
        - The response for this would be first 200, which means that the form shows up 'OK'
        - Then, we test that the creation was succesfull, which means that the code should be 302 (was redirected to home) 
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_task'), {'name': 'New Task', 'event': self.event.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_edit_task_view(self):
        """ Test for: editing a task
         - First, the response should be 200, indicating that the form is displayed correctly.
         - Then, after editing the task, the response should be 302, indicating a successful redirect.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {'name': 'Updated Task', 'event': self.event.id})
        self.assertEqual(response.status_code, 302) 

    def test_delete_task_view(self):
        """ Test for: deleting a task
         - First, the response should be 200, indicating that the form is displayed correctly.
         - Then, after deleting the task, the response should be 302, indicating a successful redirect.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Test Task').exists())   

    def test_edit_task_invalid_form(self):
        """ Test for: editing a task with invalid form data
        - First, the response should be 200, indicating that the form is displayed correctly.
        - Then, after submitting the invalid form, the response should still be 200, indicating that the form is redisplayed with errors.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {})  # Submit empty form data
        self.assertEqual(response.status_code, 200)

    def test_delete_task_nonexistent_task(self):
        """ Test for: attempting to delete a task that does not exist
        - The response should be 404, indicating that the task was not found.
        """
        self.client.force_login(self.user)
        nonexistent_task_id = 12345  # An ID that doesn't exist
        response = self.client.post(reverse('task_delete', args=[nonexistent_task_id]))
        self.assertEqual(response.status_code, 404)