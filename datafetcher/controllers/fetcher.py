"""
This module is designed to be the main comunicator with the API the app
is using.
"""
import datetime
import requests
import os

from datafetcher.oauthclient import credentialutil, oauth2api
from datafetcher.oauthclient.model.model import environment

from pyrate_limiter import Duration, RequestRate, Limiter

rate_limits = (
      RequestRate(60, Duration.HOUR), # 10 requests per hour
      RequestRate(100, Duration.DAY), # 100 requests per day
      RequestRate(4000, Duration.MONTH), # 4000 requests per month
)

limiter = Limiter(*rate_limits)

class EANAPICommunicator():
    """_summary_
    """
    def __init__(self):
        self.ean_lookup_url = """https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/"""

    @limiter.ratelimit('EANapicalls')
    def request_ean_lookup(self, ean):
        """_summary_

        Args:
            ean (_type_): _description_

        Returns:
            _type_: _description_
        """
        headers = {
                   "X-RapidAPI-Key": os.environ['RAPIDAPI_KEY'],
                   "X-RapidAPI-Host": "product-lookup-by-upc-or-ean.p.rapidapi.com"
                }
        def_url = self.ean_lookup_url + str(ean)
        response = requests.get(def_url, headers=headers)
        return response.json()


class EBAYCommunicator():
    """_summary_
    """
    def __init__(self, game_name):
        self.base_url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?'
        self.payload = {
            "q": game_name,
            "category_ids": 139973
           }
        self.token = None
        self.headers = None
        self.response = None
        self.JSON_response = None

    def get_oauth_token(self):
        api_connector = oauth2api.oauth2api()
        credentialutil.credentialutil.load('datafetcher/oauthclient/ebay-config-sample.json')
        self.token = api_connector.get_application_token(
                                                         environment.PRODUCTION,
                                                         ['https://api.ebay.com/oauth/api_scope'])
        return self.token

    def request_info(self):
        if self.token is None or self.token.token_expiry < datetime.datetime.utcnow():
            self.get_oauth_token()
        self.headers = {
                   "Authorization": "Bearer " + self.token.access_token
                }
        self.response = requests.get(self.base_url, params=self.payload, headers=self.headers)

    def get_avg_price(self):
        self.json_response = self.response.json()['itemSummaries']
        values = []
        for game in self.json_response:
            values.append(float(game['price']['value']))
        return sum(values) / len(values)
