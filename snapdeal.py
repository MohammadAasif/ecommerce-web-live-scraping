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
proxies = {'https': random.choice(proxies_list)}


searchResultsSnapdeal = []


def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)




def snapdealsearch(key):
    global headers
    global proxies_list
    global proxies
    global searchResultsSnapdeal
    
    
    writeToFire("Fetching Snapdeal Search Results")
    url = "https://www.snapdeal.com/search?"+urllib.parse.urlencode({'keyword':""+key})+"&sort=rlvncy"
    page = requests.get(url,headers=headers) #, proxies=proxies)
    soup = BeautifulSoup(page.content,"html.parser");

    print('Atleast Reached Snapdeal function')

    print(soup.find_all("div", {"class": "product-tuple-listing"}))
    for review in soup.find_all("div", {"class": "product-tuple-listing"}):
        item ={}
        name = None
        pic = None
        href =None
        price = None
        
        #print(review.find("a", {"class":"dp-widget-link" } ).text)
        name = review.find("p", {"class":"product-title" } ).text
        href= review.find("a", {"class":"dp-widget-link" } )['href']

        pic = review.find("source", {"class":"product-image" } )['srcset']
        price = review.find("span", {"class":"product-price" } ).text
        ecom = "flipkart"

        print("====SNAP===")
        print(review.find("p", {"class":"product-title" } ).text)
        print("====SNAP===")

        if(name is not None and pic is not None):
            item['name'] = name
            item['pic'] = pic
            item['ecom'] = ecom
            item['href'] = href
            item['cost'] = price
            
            print("------------------------------")
            print(review.find("a", {"class":"dp-widget-link" } )['href'])
            print(review.find("p", {"class":"product-title" } ).text)
            print(review.find("source", {"class":"product-image" } )['srcset'])
            print("------------------------------")
            
            searchResultsSnapdeal.append(item)
            
  
    print("Snapdeal Done");
    writeToFire("Snapdeal Completed")
    writeToFire("All Done")
    return searchResultsSnapdeal
