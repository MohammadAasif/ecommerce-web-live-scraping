import pyrebase
from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import json
import time


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
#80.241.219.244:3128

proxies = {'https': '89.203.250.164:3128'} #random.choice(proxies_list)}

searchResultsAmazon = []

def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)

    
def amazonsearch(key):
    global headers
    global proxies_list
    global proxies
    global searchResultsAmazon

    writeToFire("Fetching Amazon Search Results")
  
    URL = "http://www.amazon.in/s/ref=?" + urllib.parse.urlencode({'field-keywords':""+key})

    search_page = requests.get(""+URL, headers=headers, proxies=proxies);
    search_soup = BeautifulSoup(search_page.content,"lxml")

    result_list = search_soup.find_all("li", {"class":"s-result-item"})

    for result in result_list:
            item = {}
            name = None
            pic = None
            asin = None
            ecom = None
            price = None
         
            
            name = result.find("h2").text
            pic = result.find("img",{})['src']
            asin = result['data-asin']
            ecom = "amazon"
            price = result.find("span", {"class":"a-color-price"}).text

            if(name is not None and pic is not None and asin is not None and ecom is not None):
                item['name'] = name
                item['pic'] = pic
                item['asin'] = asin
                item['ecom'] = ecom
                item['cost'] = price
                print("______________________________")
                print(item)
                print("______________________________")
                searchResultsAmazon.append(item)

                          
    
    print("Amazon Stuff Done")
    writeToFire("Amazon Completed")
    return searchResultsAmazon
