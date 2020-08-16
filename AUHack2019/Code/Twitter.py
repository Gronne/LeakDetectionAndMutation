from TwitterAPI import TwitterAPI


class Twitter:
    def __init__(self):
        self.CONSUMER_KEY = ''
        self.CONSUMER_SECRET = ''
        self.ACCESS_TOKEN_KEY = ''
        self.ACCESS_TOKEN_SECRET = ''


    def post_picture_twitter(self, picture_address, TweetText):
        api = TwitterAPI(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN_KEY, self.ACCESS_TOKEN_SECRET)

        picture = self._load_leak_picture(picture_address)

        r = api.request('statuses/update_with_media', {'status': TweetText}, {'media[]': picture})
        print(r.status_code)


    def generate_product_description(self, product_keyword_list, models_3d):
        keyword = []

        for product in product_keyword_list:
            if product[0] == models_3d[0][0].strip("ID: "):
                keyword = product[1]

        twitterString = '(test)Is this the new '
        for word in keyword[:-1]:
            twitterString += word + ", "
        twitterString += keyword[-1] + "?"

        return twitterString


    def _load_leak_picture(self, pictureAddress):
        file = open(pictureAddress, 'rb')
        data = file.read()
        return data








    #Nothing
