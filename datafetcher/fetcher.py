"""
This module is designed to be the main comunicator with the API the app
is using.
"""

import requests


class APICommunicator():
    """_summary_
    """
    def __init__(self):
        self.ean_lookup_url = """https://product-lookup-by-upc-or-ean.
        p.rapidapi.com/code/"""

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
        response = requests.request("GET", def_url, headers=headers)
        return response
