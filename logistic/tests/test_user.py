from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from logistic.models import Event
from django.utils import timezone
from django.test import Client


class UserViewTests(TestCase):
    # Corrección: Asegúrate de limpiar la base de datos antes de ejecutar esta prueba
    def setUp(self):
        User.objects.all().delete()

    def test_signup_view_get(self):
        """
        Tests that the signup page loads correctly using the GET method.
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_signup_view_post_success(self):
        """
        Tests successful user registration using the POST method.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('home'))

    def test_signup_view_post_password_mismatch(self):
        """
        Tests the user registration fails with a password mismatch.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        })
        self.assertEqual(User.objects.count(), 0)
        self.assertContains(response, "Passwords do not match")

    def test_signin_view_post_success(self):
        """
        Tests successful user login using the POST method.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': '12345',
        })
        self.assertRedirects(response, reverse('home'))

    def test_signout_view(self):
        """
        Tests that the user can log out.
        """
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('signin'))

    def test_user_profile_view_authenticated(self):
        """
        Tests that the user profile page loads for authenticated users.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user')

    def test_user_profile_view_unauthenticated(self):
        """
        Tests that unauthenticated users are redirected from the user profile page.
        """
        response = self.client.get(reverse('user_profile'))
        self.assertRedirects(
            response, f"{reverse('signin')}?next={reverse('user_profile')}")

    def test_delete_user_unauthenticated(self):
        """
        Tests that unauthenticated users are redirected from the delete user page.
        This ensures that only authenticated users can attempt to delete their account.
        """
        response = self.client.post(reverse('delete_user'))
        # Expect the user to be redirected to the sign-in page, as they're not authenticated
        self.assertRedirects(
            response, f"{reverse('signin')}?next={reverse('delete_user')}")

    def test_delete_user_authenticated(self):
        """
        Tests that an authenticated user can delete their account and is then redirected to the sign-in page.
        This test first logs in a test user, then sends a POST request to delete the user,
        and finally verifies that the user no longer exists in the database.
        """
        # Creating a user directly in the database
        user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='12345')

        # Logging in the user
        self.client.login(username='testuser', password='12345')

        # The user should exist at this point
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Sending a POST request to the 'delete_user' view to delete the authenticated user
        response = self.client.post(reverse('delete_user'))

        # After deletion, the user should no longer exist
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # The response should be a redirect to the sign-in page
        self.assertRedirects(response, reverse('signin'))

    def test_search_user_view_get(self):
        """
        Test that the search user page loads correctly using the GET method.
        """
        response = self.client.get(reverse('users_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_search.html')

    def test_search_user_view_post_username(self):
        """
        Test searching for users by username.
        """
        # Create some test users
        user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='password123')
        user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='password456')
        user3 = User.objects.create_user(
            username='user3', email='user3@example.com', password='password789')

        # Perform a POST request to search for users by username
        response = self.client.post(reverse('users_search'), {
            'search_query': 'user1'
        })
        self.assertEqual(response.status_code, 200)
        # Ensure user1 is in the response
        self.assertContains(response, 'user1')
        self.assertNotContains(response, 'user2')
        self.assertNotContains(response, 'user3')

    def test_search_user_view_post_id(self):
        """
        Test searching for users by ID.
        """
        # Create some test users
        user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='password123')
        user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='password456')
        user3 = User.objects.create_user(
            username='user3', email='user3@example.com', password='password789')

        # Perform a POST request to search for users by ID
        response = self.client.post(reverse('users_search'), {
            'search_query': user2.id
        })
        self.assertEqual(response.status_code, 200)
        # Ensure user2 is in the response
        self.assertContains(response, 'user2')
        self.assertNotContains(response, 'user1')
        self.assertNotContains(response, 'user3')

    def test_search_user_view_post_no_results(self):
        """
        Test searching for users with no results.
        """
        # Perform a POST request to search for a non-existent user
        response = self.client.post(reverse('users_search'), {
            'search_query': 'nonexistent'
        })
        self.assertEqual(response.status_code, 200)
        # Ensure the response indicates no results found
        self.assertContains(response, '')
