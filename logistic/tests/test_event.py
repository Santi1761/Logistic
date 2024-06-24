from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from logistic.models import Event
from django.contrib.auth.models import User
from datetime import timedelta


class TestEvent(TestCase):
    # Creamos un usuario y evento para probar los métodos
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.event = Event.objects.create(name='Test Event', executionDate=timezone.now(
        ) + timedelta(days=7), place='Test Place', progress=0, user=self.user)

    def test_create_event(self):
        """ Test for: creating a new event in the database.

        - First, we authenticate the user with force_login.
        - Then, we capture the response of the page when creating the event.
        - Finally, after creating the event, the status code of the page would be 200, which is 'OK' and means that the request was successful.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_event'), {'name': 'New Event', 'executionDate': timezone.now(
        ) + timedelta(days=7), 'place': 'New Place', 'progress': 0})
        self.assertEqual(response.status_code, 200)

    def test_create_event2(self):
        """ Test for: Creating a new event with a not valid input

        - The response of this would be 200, since the request was succesfull
          and it doesn't show up any unexpected error, just the normal ValueError that is controled
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_event'), {
                                    'name': 'New Event2', 'executionDate': "valorNoValido", 'place': 'Hall de auditorios', "progress": 20})
        self.assertEqual(response.status_code, 200)

    def test_create_event3(self):
        """Test for: create event with missing arguments
        - In this test we are not gonna give the name for creating the event.
        - The response of this would be 200, siince the form is validated.
        - It's supposed to not show up any unexpected error. 
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_event'), {'executionDate': timezone.now(
        ) + timedelta(days=7), 'place': 'New Place', 'progress': 0})
        self.assertEqual(response.status_code, 200)

    def test_edit_event(self):
        """ Test for: edit an event already created
        - The response of this would be 200, since the edit was made succesfully
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_event', args=[self.event.id]), {
                                    'name': 'Updated Event', 'executionDate': timezone.now() + timedelta(days=14), 'place': 'Updated Place', 'progress': 50})
        self.assertEqual(response.status_code, 200)

    def test_edit_event2(self):
        """Test for: edit an event that doesn't exit
        - We use and Id that does not correspond to any event.
        - The response of this would be 404, page not found, because the event does not exit
        """
        self.client.force_login(self.user)
        event_id_non_exist = 123
        response = self.client.post(reverse('edit_event', args=[event_id_non_exist]), {
                                    'name': 'Updated Event That Not Exist', 'executionDate': timezone.now() + timedelta(days=7), 'place': 'Updated Place 2', 'progress': 80})
        self.assertEqual(response.status_code, 404)

    def test_edit_event3(self):
        """Test for: edit event with invalid data
        - The response of this would be 200, since the form is validated
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_event', args=[self.event.id]), {
                                    'name': 'Updated Event', 'executionDate': "invalid date", 'place': 'Updated Place', 'progress': 50})
        self.assertEqual(response.status_code, 200)

    def test_complete_event(self):
        """Test for: mark an event as completed
        - The response of this would be 302, which means is redirected to another page temporally
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('event_complete', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)

    def test_complete_event2(self):
        """Test for: mark an event that doesn't exist as completed
        - The response of this would be 404, which means that the event wasn't found
        """
        self.client.force_login(self.user)
        event_id_non_exist = 123
        response = self.client.post(
            reverse('event_complete', args=[event_id_non_exist]))
        self.assertEqual(response.status_code, 404)

    def test_delete_event(self):
        """Test for: delete an event
        - The response of this would be 302, which means is redirected to home
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('event_delete', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_event2(self):
        """Test for: delete an event that doesn't exist
        - The response of this would be 404, which means that the event wasn't found
        """
        event_id_non_exist = 123
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('event_delete', args=[event_id_non_exist]))
        self.assertEqual(response.status_code, 404)

    def test_access_other_user_event(self):
        """Test for: Validate that no user can access to an event that does not correspond to him/her
        - The respond of this would be 302, since the user has no access to it and teh method return error 302
        - For this, we have to add another user and another event to that user
        - The user that is in the BD is going to try to acces to the event that belongs to "other_user"
        """
        other_user = User.objects.create_user(
            username='otheruser', password='12345')
        other_user_event = Event.objects.create(name='Other User Event', executionDate=timezone.now(
        ) + timedelta(days=7), place='Test Place', progress=0, user=other_user)
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_event', args=[other_user_event.id]), {
                                    'name': 'Updated Event', 'executionDate': timezone.now() + timedelta(days=14), 'place': 'Updated Place', 'progress': 50})
        self.assertEqual(response.status_code, 302)

    def test_delete_event3(self):
        """Test for: Delete event twice
        - We are going to delete an event once
        - The, we'll try to delete it again
        - The first response should be 302, which means that the user was redirected to home
        - The second response should be 404, which means that couldn't find the event, because was already deleted
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('event_delete', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse('event_delete', args=[self.event.id]))
        self.assertEqual(response.status_code, 404)
