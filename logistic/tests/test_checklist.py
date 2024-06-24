from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from logistic.models import Event
from logistic.models import Task
from logistic.forms.taskForm import TaskChecklist


class TestsEventChecklist(TestCase):
    def setUp(self):
        """
        Sets up the test environment by creating users, events, and tasks.
        """
        # User creation
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass')

        # Event and task creation with mandatory fields
        self.event = Event.objects.create(
            name='Test Event',
            user=self.user,
            executionDate=timezone.now(),
            finishDate=timezone.now() + timezone.timedelta(days=1),
            place='Test Place',
            progress=50,
            important=False
        )
        self.task1 = Task.objects.create(
            name='Test Task 1', event=self.event, done=False)
        self.task2 = Task.objects.create(
            name='Test Task 2', event=self.event, done=True)

        # Test client setup
        self.client = Client()

    def test_access_by_superuser(self):
        """
        Verifies that a superuser can access the event checklist.
        """
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(
            reverse('event_checklist', kwargs={'event_id': self.event.id}))
        self.assertEqual(response.status_code, 200)

    def test_access_by_event_owner(self):
        """
        Verifies that the event owner can access their checklist.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse('event_checklist', kwargs={'event_id': self.event.id}))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_other_users(self):
        """
        Ensures users who are not the event owner or superusers are denied access.
        """
        other_user = User.objects.create_user(
            username='otheruser', password='12345')
        self.client.login(username='otheruser', password='12345')
        response = self.client.get(
            reverse('event_checklist', kwargs={'event_id': self.event.id}))
        self.assertEqual(response.status_code, 404)

    def test_post_valid_formset(self):
        """
        Tests updating tasks through a valid formset and verifies redirection.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('event_checklist', kwargs={'event_id': self.event.id}), {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-0-id': str(self.task1.id),
            'form-0-done': 'on',
            'form-1-id': str(self.task2.id),
            'form-1-done': '',
        })
        self.assertRedirects(response, reverse('home'))

    def test_get_event_checklist(self):
        """
        Checks that the event checklist view returns the expected context.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse('event_checklist', kwargs={'event_id': self.event.id}))
        self.assertTrue('formset' in response.context)
        self.assertTrue('event' in response.context)
        self.assertEqual(response.context['event'], self.event)
