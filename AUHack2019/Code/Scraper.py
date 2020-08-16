import urllib.request
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        pass

    def get_pictures_urls(self, url):
        html_page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_page, "lxml")

        url_list = []
        for img in soup.findAll('img'):
            url_list.append(url + img.get('src'))
            print(img)

        return url_list


    def download_pictures(self, picture_urls, saving_address, core_name):
        picture_addresses = []

        for counter, picture_url in enumerate(picture_urls):
            print(picture_url)
            try:
                full_path = saving_address + core_name + str(counter) + ".PNG"
                picture_addresses.append(full_path)

                urllib.request.urlretrieve(picture_url, full_path)
            except:
                pass

        return picture_addresses







#Nothing
