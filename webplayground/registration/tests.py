
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
# Create your tests here.

class MessengerTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'pasword')

    def test_profile_exist(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)


