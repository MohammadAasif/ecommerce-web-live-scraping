import pyrebase
from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver

analyzer = SentimentIntensityAnalyzer()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
#proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
proxies_list = ["177.184.196.59:8080","36.81.184.160:80","66.254.177.146:3128","200.229.202.147:8080","93.139.212.80:8080"]
proxies = {'https': random.choice(proxies_list)}


#firebase init
config = {
    "apiKey": "AIzaSyDtBm6_TmofFu2J6J4B30G0hjHVfl89PYs",
    "authDomain": "senti-a92bc.firebaseapp.com",
    "databaseURL": "https://senti-a92bc.firebaseio.com",
    "storageBucket": "senti-a92bc.appspot.com"
}

firebase = pyrebase.initialize_app(config)
firedb = firebase.database()


def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)


def snapdealreviews(href):
    pageNoSnap =1
    rev_snapdeal = []
    
    while True:
        if(pageNoSnap >3):
            break
        url = href + "/reviews?page="+str(pageNoSnap)

        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,"html.parser");

        for review in soup.find_all("div", {"class": "user-review"}):
            print("------------------------------")
            if(True):
                item ={}
                item['review'] = str(review.find("p").text)[:200]
                sentimenta = analyzer.polarity_scores(str(review.find("p").text))
                POS = sentimenta['pos']
                NEU = sentimenta['neu']
                NEG = sentimenta['neg']
                pos= int(float(POS) * 10000)
                neg= int(float(NEG) * 10000)
                neu = int(float(NEU) * 10000)
                if pos>neg:# and pos>neu:
                    #senticountPOS = senticountPOS + 1
                    item['sentiment'] = "Positive"
                elif neg>pos:# and neg>neu:
                    #senticountNEG = senticountNEG - 1
                    item['sentiment'] = "Negative"
                else:
                    item['sentiment'] = "Neutral"
                rev_snapdeal.append(item)
                print(review.find("p").text)
                #ata.append(item)
                print("------------------------------")

        pageNoSnap = pageNoSnap +1        

    return rev_snapdeal
    

    
