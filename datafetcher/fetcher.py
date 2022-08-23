"""
This module is designed to be the main comunicator with the API the app
is using.
"""
import requests


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
                   "X-RapidAPI-Key": "7c75f38fb8msh35fac229235b7d3p1eab49jsnf4e0ea729333",
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
        self.headers = headers = {
                   "Authorization": "Bearer v^1.1#i^1#f^0#p^3#r^0#I^3#t^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"
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
