import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from accounts.models import CustomUser
from collection.models import Collection


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
        Collection.objects.create(name='My First Collection', user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_login(self):
        # getting file to upload
        cwd = os.getcwd()
        image_path = os.path.join(cwd, 'tests/unit_tests/media_test/barcode.png')

        # going to upload url
        self.selenium.get(f'{self.live_server_url}/barcode/upload')
        file_input = self.selenium.find_element(By.NAME, "file")
        file_input.send_keys(image_path)

        self.selenium.find_element(By.XPATH, '//*[@id="upload-button"]').click()
        assert "Rockstar Games Grand Theft Auto" in self.selenium.page_source
