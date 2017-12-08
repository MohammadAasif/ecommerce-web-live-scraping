from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
import pyrebase
analyzer = SentimentIntensityAnalyzer()

from amazon import amazonsearch
from flipkart import flipkartsearch
from snapdeal import snapdealsearch

from review_amazon import amazonreviews
from review_flipkart import flipkartreviews
from review_snapdeal import snapdealreviews


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


analyzer = SentimentIntensityAnalyzer()
app = Flask(__name__)
key = ""


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
proxies = {'https': random.choice(proxies_list)}

searchResultsAmazon = []
searchResultsFlipkart = []
searchResultsSnapdeal = []


REVIEWSTUB = []

 
def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)



def allsearches():
    global searchResults
    global searchResultsAmazon
    global searchResultsFlipkart
    global searchResultsSnapdeal
    global key
    
    searchResultsAmazon = []
    searchResultsFlipkart = []
    searchResultsSnapdeal = []

    writeToFire("Initiating searches")
    searchResultsAmazon = amazonsearch(key)
    searchResultsFlipkart = flipkartsearch(key)
    searchResultsSnapdeal = snapdealsearch(key)


#Start of main#
@app.route('/')
def main():
    return render_template('index.html')
 
@app.route('/search',methods=['POST','GET'])
def search():
    global key
    postData = request.json
    key = postData['key']
    print("Search Key: "+key);

    #all the searches
    allsearches()
    
    print("All Done")
    searchResults = { "amazon": searchResultsAmazon, "flipkart": searchResultsFlipkart, "snapdeal":searchResultsSnapdeal}
    return json.dumps(searchResults)


@app.route('/senti',methods=['POST','GET'])
def senti():
    global REVIEWSTUB
    global proxies
    global headers
    params = request.json


    overallsenti =""
    senticountPOS = 0
    senticountNEG = 0

    print("=====================Sent packet================")
    print(params)
 
    amazon = params['amazon']
    flipkart = params['flipkart']
    snapdeal = params['snapdeal']
   
    data =[]

    if("asin" in amazon):
        asin = amazon['asin']
        data =  data + amazonreviews(asin)
        
    if("href" in flipkart):
        link = flipkart['href']
        s = link.split("#")[0]
        s = s.split("?")[0]

        s = "https://www.flipkat.com" + s

        data = data + flipkartreviews(s)
        
    if("href" in snapdeal):
        link = snapdeal['href']
        snaphref = link.split("#")[0]
        snaphref = snaphref.split("?")[0]

        data =  data + snapdealreviews(snaphref)

    REVIEWSTUB = data
    '''
    print("######PARAMS##########################")
    print(params)
    print("################################")

    percentage = None
    overall = ""
    if senticountPOS > senticountNEG:
        overall="Positive"
        aller= senticountPOS + senticountNEG
        per = senticountPOS / aller
        per = per * 100
        percentage = per #(((float)senticountPOS)/((float)senticountPOS +(float)senticountNEG))*100
    else:
        overall = "Negative"
        aller= senticountPOS + senticountNEG
        per = senticountNEG / aller
        per = per * 100
        percentage = per
        
    newdata = {"data":data, "overall":overall,"percentage":percentage}
    REVIEWSTUB = newdata
    '''
    return json.dumps(data) #newdata) #render_template('review.html')



@app.route("/revpage", methods=['GET','POST'])
def revpage():
    print("REV PAGE REACHED")     
    return render_template('review.html')

 
@app.route("/getreviews", methods=['GET','POST'])
def getrev():
    global REVIEWSTUB

    POS = 0
    NEG =0

    for rev in REVIEWSTUB:
        if(rev['sentiment'] == "Positive"):
            POS = POS + 1
        else:
            NEG = NEG +1
            

    overall = None
    percent = None
    if(POS>NEG):
        overall = "Positive"
        percent = ( (POS/(POS+NEG))* 100)
    else:
        overall = "Negative"
        percent = ( (NEG/(POS+NEG))* 100)

    return json.dumps({"data":REVIEWSTUB,"overall":overall,"percent":percent})

    
    
if __name__ == '__main__':
    app.run(debug=True)
