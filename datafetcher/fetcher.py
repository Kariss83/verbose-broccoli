"""
This module is designed to be the main comunicator with the API the app
is using.
"""
import requests
import os


class EANAPICommunicator():
    """_summary_
    """
    def __init__(self):
        self.ean_lookup_url = """https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/"""

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
        return response


class EBAYCommunicator():
    """_summary_
    """
    def __init__(self, game_name):
        self.base_url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?'
        self.payload = {
            "q":  game_name,
            "category_ids":  139973
           }
        self.oauth_token = None
        self.headers = headers = {
                   "Authorization": self.oauth_token
                }
        self.response = None
        self.JSON_response = None

    def get_api_token(self):
        pass

    def request_info(self):
        self.response = requests.get(self.base_url, params=self.payload, headers=self.headers)

    def get_avg_price(self):
        self.json_response = self.response.json()['itemSummaries']
        values = []
        for game in self.json_response:
            values.append(float(game['price']['value']))
        return sum(values)/len(values)

    # def get_avg2(self):

    #     self.json_response = self.response.json()['itemSummaries']
    #     avg = reduce(lambda x, y: x + float(y['price']['value']), self.json_response, 0) / len(self.json_response)
    #     return avg
