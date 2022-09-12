import os
from unittest import mock
from datetime import datetime, timedelta


from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from accounts.models import CustomUser
from collection.models import Collection
from datafetcher import constants
from datafetcher.oauthclient.model.model import oAuth_token


opts = FirefoxOptions()
opts.add_argument("--headless")


def create_an_user(number):
    user_test = CustomUser.objects.create(
        email=f"test{number}@gmail.com", username=f"MRTest{number}"
    )
    return user_test


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" in args[0]:
        return MockResponse(constants.EAN_API_RETURN, 200)
    elif args[0] == "https://api.ebay.com/buy/browse/v1/item_summary/search?":
        return MockResponse(constants.EBAY_RETURN, 200)

    return MockResponse(None, 404)


def mocked_get_application_token(*args, **kwargs):
    token = oAuth_token()
    token.access_token = "myfaketoken"
    token.token_expiry = datetime.utcnow() + timedelta(hours=5) - timedelta(minutes=5)
    return token


def mocked_credential_load(*args, **kwargs):
    pass


class UserUploadTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)
        cls.user = create_an_user(1)
        cls.user.set_password("monsupermotdepasse")
        cls.user.save()
        Collection.objects.create(name="My First Collection", user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @mock.patch(
        "datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "datafetcher.controllers.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_can_upload_a_file(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        # getting file to upload
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/barcode.png")

        # going to upload url
        self.selenium.get(f"{self.live_server_url}/barcode/upload")
        file_input = self.selenium.find_element(By.NAME, "file")
        file_input.send_keys(image_path)

        self.selenium.find_element(By.XPATH, '//*[@id="upload-button"]').click()
        assert "Le Seigneur des anneaux" in self.selenium.page_source
