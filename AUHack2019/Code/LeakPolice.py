from Twitter import Twitter
from Scraper import WebScraper
from Detecters import *
from FileManagement import FilePictureManagement
from Mutate import Model3DMutater
from Modeling import *

import random
from datetime import datetime
import os


random.seed(datetime.now())


url = "https://legoleaktest.firebaseapp.com/"
address = os.path.dirname(os.path.abspath(__file__)) + "\\..\\"
download_address = "Pictures/Downloaded/"
lego_rec_address = "Pictures/LegoRec/"
leak_rec_address = "Pictures/LeakRec/"
mutation_address = "Pictures/Mutations/"
rotation_address = "Pictures/Rotated/"
models_3d_address = "Models3D/"


FP               = FilePictureManagement()
scraper          = WebScraper()
lego_detect      = LegoDetecter(FP)

models_3D        = Modeling3D(address + models_3d_address)
models_adaptions = ModelAdaption(FP, models_3D, address + rotation_address)
leak_detect      = LeakDetecter(FP, models_adaptions)

mutater          = Model3DMutater(FP, models_3D, models_adaptions, address + mutation_address)
twitter_upload   = Twitter()


picture_urls = scraper.get_pictures_urls(url)
picture_addresses = scraper.download_pictures(picture_urls, address + download_address, "DownloadedPicture")

lego_picture_addresses = lego_detect.detect_lego_pictures(picture_addresses)
FP.move_pictures(lego_picture_addresses, address + lego_rec_address)

[leak_picture_addresses, leak_snapshot_addresses] = leak_detect.detect_leak_pictures(lego_picture_addresses, 0.7)
FP.move_pictures(leak_picture_addresses, address + leak_rec_address)

mutated_leak_addresses = mutater.mutate_models(leak_snapshot_addresses)

#---------------Post to twitter---------------
product_keyword_list = [['23f2f42ffsfg', ['Lego', 'Star Wars', 'Cube']]]

random_number = random.randint(0, len(mutated_leak_addresses) - 1)
fake_leak_picture_address = mutated_leak_addresses[random_number]

twitter_string = twitter_upload.generate_product_description(product_keyword_list, models_3D.get_models_3d())
#twitter_upload.post_picture_twitter(fake_leak_picture_address, twitter_string)

print(twitter_string)
print(fake_leak_picture_address)
