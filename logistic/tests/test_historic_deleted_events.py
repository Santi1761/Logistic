from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from logistic.models import HistoricDeletedEvents

class TestHistoricDeletedEvents(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(username='superuser', password='12345')
        self.client = Client()

    def test_historic_deleted_events_pagination(self):
        # Create more than the default number of historic deleted events
        for i in range(15):
            HistoricDeletedEvents.objects.create(
                name=f'Test Event {i}',
                executionDate=timezone.now(),
                place='Test Place',
                progress=0,
                user=self.user,
                deleted=timezone.now().date()
            )

        # Log in the user
        self.client.force_login(self.user)

        # Access the view for historic deleted events
        response = self.client.get(reverse('historic_deleted_events'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct number of events are present in the context
        expected_events_count = HistoricDeletedEvents.objects.count()
        self.assertEqual(len(response.context['historic_events']), expected_events_count)

    def test_historic_deleted_events_pagination_superuser(self):
        # Log in the superuser
        self.client.force_login(self.superuser)

        # Access the view for historic deleted events
        response = self.client.get(reverse('historic_deleted_events'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if all events are present for superuser
        self.assertEqual(len(response.context['historic_events']), HistoricDeletedEvents.objects.count())

   
