from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from logistic.models import Event
from logistic.views.event import delete_event
from logistic.views.event import complete_event

class views_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        self.event = Event.objects.create(
            name='Test Event',
            executionDate=timezone.now(),
            place='Test Place',
            progress=50,
            finishDate=timezone.now(),
            important=True,
            user=self.user
        )
    

   
           
    def test_edit_event(self):
        url = reverse('edit_event', args=[self.event.pk])
        data = {
            'name': 'Updated Event',
            'executionDate': '2022-12-31T23:59',
            'place': 'Updated Place',
            'progress': 75,
            'finishDate': '2023-01-01T00:01',
            'important': False,
            'user': self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')

    def test_delete_event(self):
        url = reverse('event_delete', args=[self.event.pk])
        request = self.factory.post(url)
        request.user = self.user
        response = delete_event(request, event_id=self.event.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)


    def test_complete_event(self):
        url = reverse('event_complete', args=[self.event.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertIsNotNone(self.event.completed)

