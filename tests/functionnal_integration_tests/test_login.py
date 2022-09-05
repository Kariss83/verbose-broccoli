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

    def test_can_login(self):
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element(By.NAME, "email")
        username_input.send_keys('test1@gmail.com')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('monsupermotdepasse')
        self.selenium.find_element(By.XPATH, '/html/body/header/div/form/p[2]/input').click()

        message = self.selenium.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('You are logged in !', message.text)


if __name__ == '__main__':
    pass
