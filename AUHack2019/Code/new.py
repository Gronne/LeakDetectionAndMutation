from TwitterAPI import TwitterAPI
from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np

#---------------Download picture---------------

def dl_img(url, file_path, file_name):
    full_path = file_path + file_name
    urllib.request.urlretrieve(url, full_path)

def findAllPictureURLS(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    imageUrlList = []
    for img in soup.findAll('img'):
        imageUrlList.append(img.get('src'))
        print(img)
    return imageUrlList

url = "https://stackoverflow.com/questions/40160789/skipping-error-404-with-beautifulsoup"
file_name = "DownloadedPicture"
type = ".PNG"
address = 'C:/Users/mathi/Desktop/AUHack2019/Pictures/'
downloadAddress = "Downloaded/"
legoRecAddress = "LegoRec/"
leakRecAddress = "LeakRec/"
mutationAddress = "Mutations/"

urlList = findAllPictureURLS(url)
#---------------Download all Pictures---------------
for counter, urlElement in enumerate(urlList):
    print(urlElement)
    try:
        dl_img(urlElement, address + downloadAddress, file_name + str(counter) + type)
    except:
        pass

#---------------Get bitmaps---------------
for counter, urlElement in enumerate(urlList):
    try:
        #Load image
        img = Image.open(address + downloadAddress + file_name + str(counter) + type)

        #Transform to np image
        ary = np.array(img)

        # Split the three channels
        r,g,b = np.split(ary,3,axis=2)
        r=r.reshape(-1)
        g=r.reshape(-1)
        b=r.reshape(-1)

        # Standard RGB to grayscale
        bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2],
        zip(r,g,b)))
        bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
        bitmap = np.dot((bitmap > 128).astype(float),255)
        im = Image.fromarray(bitmap.astype(np.uint8))

        #Save LegoRec images
        im.save(address + legoRecAddress + file_name + str(counter) + type)

        #Save LeakRec imageUrl
        im.save(address + leakRecAddress + file_name + str(counter) + type)

    except:
        print("Not able to manipulate image: " + str(counter))


#---------------     Mutate    ---------------


#---------------Post to twitter---------------
def postPictureToTwitter(pictureAddress, TweetText):
    CONSUMER_KEY = 'sdwpZS1BGDaSpKnF8bqkuGkFz'
    CONSUMER_SECRET = 'HvvmvR2lMMgTNLFdRXLRffGm05B2OT5pFLnC5erTaw4q62aMjA'
    ACCESS_TOKEN_KEY = '719103880819314688-Z3Pa4gCG8PJrHJ3Q6NpxW8d9MYzrSfp'
    ACCESS_TOKEN_SECRET = 'WCV2GLNIs3gKQODRmTFVEwIsCUxqZk8hTWHXQb1JwcgWg'

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    file = open(pictureAddress + type, 'rb')
    data = file.read(pictureAddress)
    r = api.request('statuses/update_with_media', {'status':TweetText}, {'media[]':data})
    print(r.status_code)

for counter, urlElement in enumerate(urlList):
    #Get product information from firebase

    #Post in twitter
    #postPictureToTwitter(address + mutationAddress + file_name + str(counter), 'What, a new picture?')
