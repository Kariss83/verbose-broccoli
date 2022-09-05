from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


def create_an_user(number):
    user_test = CustomUser.objects.create(
            email=f"test{number}@gmail.com",
            username=f"MRTest{number}"
        )
    return user_test


class UserLoginTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)
        cls.user = create_an_user(1)
        cls.user.set_password('monsupermotdepasse')
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_create_an_account(self):
        self.selenium.get(f'{self.live_server_url}/accounts/register/')
        assert "Create your account" in self.selenium.page_source
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys('test2@gmail.com')
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('MRTest')
        password_input = self.selenium.find_element(By.NAME, "password1")
        password_input.send_keys('monsupermotdepasse')
        password_input = self.selenium.find_element(By.NAME, "password2")
        password_input.send_keys('monsupermotdepasse')
        self.selenium.find_element(By.XPATH, '/html/body/header/div/form/div[5]/input').click()

        message = self.selenium.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('You are now signed in...', message.text)
