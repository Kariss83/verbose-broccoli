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


class UserLoginLogOutTest(StaticLiveServerTestCase):
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

    def test_can_login_then_log_out(self):
        # login in
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element(By.NAME, "email")
        username_input.send_keys('test1@gmail.com')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('monsupermotdepasse')
        self.selenium.find_element(By.XPATH, '/html/body/header/div/form/p[2]/input').click()
        # checking for success message
        message = self.selenium.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('You are logged in !', message.text)
        # going to my profile
        navbar_button = self.selenium.find_element(By.XPATH, '//*[@id="expand-button"]')
        self.selenium.execute_script(
            'arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";',
            navbar_button
        )
        navbar_button.click()
        profile_link = self.selenium.find_element(By.LINK_TEXT, 'My Profile')
        profile_link.click()

        assert "MRTest1" in self.selenium.page_source

        # click on logout
        self.selenium.find_element(By.XPATH, '//*[@id="Logout"]').click()
        # look for alert on disconnection
        message = self.selenium.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('You are disconnected...', message.text)
