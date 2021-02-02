import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from helper import keys
from main.models import UserData

client = Client()


class UserSignupTestCase(TestCase):
    """
    Test cases for user signup
    """
    def setUp(self):
        self.payload_invalid_username = {keys.USERNAME: 'A$3'}
        self.payload_invalid_password = {keys.USERNAME: 'bhirendra', keys.PASSWORD: ' 1 g  % '}
        self.payload_invalid_email = {keys.USERNAME: 'bhirendra', keys.PASSWORD: 'Bhi#1', keys.EMAIL: 'a.com'}
        self.payload_invalid_mobile = {keys.USERNAME: 'bhirendra', keys.PASSWORD: 'Bhi#1', keys.EMAIL: '', keys.MOBILE: '1234567890'}
        self.payload_valid_user = {keys.USERNAME: 'bhi123', keys.PASSWORD: 'Bhi#1', keys.EMAIL: 'bhirendra2014@gmail.com', keys.MOBILE: '9907890199'}

    def test_signup(self):
        """
        Test cases for user-signup API
        :return:
        """
        """ Invalid username """
        response1 = client.post(reverse('user-signup'), data=json.dumps(self.payload_invalid_username), content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        """ Invalid password """
        response2 = client.post(reverse('user-signup'), data=json.dumps(self.payload_invalid_password), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        """ Invalid email """
        response3 = client.post(reverse('user-signup'), data=json.dumps(self.payload_invalid_email), content_type='application/json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        """ Invalid mobile """
        response4 = client.post(reverse('user-signup'), data=json.dumps(self.payload_invalid_mobile), content_type='application/json')
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        """ Valid User """
        response5 = client.post(reverse('user-signup'), data=json.dumps(self.payload_valid_user), content_type='application/json')
        self.assertEqual(response5.status_code, status.HTTP_200_OK)


class UserLoginTestCase(TestCase):
    """
    Test cases for user login
    """
    def setUp(self):
        self.saved_username = 'Bhi123'
        self.saved_password = 'Bhi#1'

        # Create user instance
        django_user = User.objects.create(username=self.saved_username)
        django_user.set_password(self.saved_password)
        django_user.save()
        UserData.objects.create(user=django_user)

        # Test payloads
        self.payload_invalid_username = {keys.USERNAME: 'A$3', keys.PASSWORD: self.saved_password}
        self.payload_invalid_password = {keys.USERNAME: self.saved_username, keys.PASSWORD: ' 1 g  % '}
        self.payload_valid = {keys.USERNAME: self.saved_username, keys.PASSWORD: self.saved_password}

    def test_login(self):
        """
        Test cases for user-login API
        :return:
        """
        """ Invalid username """
        response1 = client.post(reverse('user-login'), data=json.dumps(self.payload_invalid_username), content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        """ Invalid password """
        response2 = client.post(reverse('user-login'), data=json.dumps(self.payload_invalid_password), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        """ Valid User """
        response5 = client.post(reverse('user-login'), data=json.dumps(self.payload_valid), content_type='application/json')
        self.assertEqual(response5.status_code, status.HTTP_200_OK)


class UserProfileTestCase(TestCase):
    """
    Test cases for user login
    """
    def setUp(self):
        self.saved_username = 'Bhi123'
        self.saved_password = 'Bhi#1'

        # Create user instance
        django_user = User.objects.create(username=self.saved_username)
        django_user.set_password(self.saved_password)
        django_user.save()
        UserData.objects.create(user=django_user)

        login_response = client.post(reverse('user-login'), data=json.dumps({
            keys.USERNAME: self.saved_username,
            keys.PASSWORD: self.saved_password
        }), content_type='application/json')

        self.saved_token = login_response._headers[keys.TOKEN][1]

        # Test payloads
        self.header_invalid_token = {keys.TOKEN: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFt1231'}
        self.header_expired_token = {keys.TOKEN: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFt3sI52135'}
        self.header_valid_token = {keys.TOKEN: self.saved_token}

    def test_profile(self):
        """
        Test cases for user-profile API
        :return:
        """
        """ Invalid username """
        response1 = client.get(reverse('user-profile'), content_type='application/json', **self.header_invalid_token)
        self.assertEqual(response1.status_code, keys.HTTP_440_LOGIN_TIME_OUT)
        """ Invalid password """
        response2 = client.get(reverse('user-profile'), content_type='application/json', **self.header_expired_token)
        self.assertEqual(response2.status_code, keys.HTTP_440_LOGIN_TIME_OUT)
        """ Valid User """
        response3 = client.get(reverse('user-profile'), content_type='application/json', **self.header_valid_token)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
