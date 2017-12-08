import pyrebase
from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import json
import time

analyzer = SentimentIntensityAnalyzer()


firebaseconfig = {
    "apiKey": "AIzaSyDtBm6_TmofFu2J6J4B30G0hjHVfl89PYs",
    "authDomain": "senti-a92bc.firebaseapp.com",
    "databaseURL": "https://senti-a92bc.firebaseio.com",
    "storageBucket": "senti-a92bc.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseconfig)
firedb = firebase.database()


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
proxies = {'https': random.choice(proxies_list)}

def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)

def amazonreviews(asin):
    pageNo = 1
    count = 0
    rev_amazon = []
    while True:
       if(pageNo >3 ):
          break
       reviews_page_url = "http://www.amazon.in/product-reviews/" + asin +"/ref=?pageNumber="+str(pageNo)
       print("URL: "+reviews_page_url)
       reviews_page =  requests.get(""+reviews_page_url, headers=headers, proxies=proxies )
       reviews_soup = BeautifulSoup(reviews_page.content,"lxml")
       reviews = reviews_soup.find_all("div",{"class":"a-section"})

       localCount =0
       for rev in reviews:
          for rev_data in rev.find_all("div",{"class":"review-data"}):
             for rev_text in rev_data.find_all("span",{"class":"review-text"}):
                    print("__________________________________________________________")
                    print(""+rev_text.text)
                    if str(rev_text.text) not in rev_amazon:
                       item ={}
                       item['review'] = str(rev_text.text)[:200]
                       sentimenta = analyzer.polarity_scores(str(rev_text.text))
                       POS = sentimenta['pos']
                       NEU = sentimenta['neu']
                       NEG = sentimenta['neg']
                       pos= int(float(POS) * 10000)
                       neg= int(float(NEG) * 10000)
                       neu= int(float(NEU) * 10000)
                       if pos>neg:# and pos>neu:
                           item['sentiment'] = "Positive"
                           #senticountPOS = senticountPOS + 1
                       elif neg>pos:# and neg>neu:
                           #senticountNEG = senticountNEG - 1
                           item['sentiment'] = "Negative"
                       else:
                           item['sentiment'] = "Neutral" 

                       rev_amazon.append(item)
                       count = count + 1
                       localCount = localCount + 1
                    print("__________________________________________________________")
       if(localCount == 0):
           break
       pageNo = pageNo + 1

    return rev_amazon

    
