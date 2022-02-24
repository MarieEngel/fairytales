from django.test import TestCase
from django.contrib.auth.models import User

class LoginLogoutTest(TestCase):

    def setUp(self):
            self.user = User.objects.create_user(
                username="testuser", password="password"
            )

    def tearDown(self):
        self.user.delete()

    def test_login(self):
        response = self.client.get('/fairytales/login/')
        self.assertEquals(response.status_code, 200)

        self.client.login(username = 'testuser', password= 'password')
        response = self.client.get('/fairytales/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Logout')
    

    def test_logout(self):
        response = self.client.get('/fairytales/logout/')
        self.assertEquals(response.status_code, 302)

        self.client.logout()
        response = self.client.get('/fairytales/')
        self.assertContains(response, 'Login')
       
