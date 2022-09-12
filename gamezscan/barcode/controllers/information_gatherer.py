from gamezscan.datafetcher.controllers import fetcher


class Gatherer:
    """This class is designed to call all the API fetcher in order to
    get full info on a given product with a barcode
    """

    def __init__(self, barcode):
        self.barcode = barcode[0]
        self.game_name = None
        self.avg_price = None
        self.image_url = None

    def get_name_and_img_url(self):
        ean_fetcher = fetcher.EANAPICommunicator()
        data = ean_fetcher.request_ean_lookup(self.barcode)
        self.game_name = data["product"]["name"]
        self.image_url = data["product"]["imageUrl"]
        return self.game_name, self.image_url

    def get_avg_price(self):
        ebay_fetcher = fetcher.EBAYCommunicator(self.game_name)
        ebay_fetcher.request_info()
        self.avg_price = ebay_fetcher.get_avg_price()
        return self.avg_price
