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

searchResultsFlipkart = []

 

PROXY = ""+random.choice(proxies_list) # IP:PORT or HOST:PORT
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % PROXY)


def writeToFire(msg):
    global firedb
    firedb.child("status").set(msg)


STUFF = []

def flipkartsearch(key):
    global STUFF
    keyword_string = key#"dell+insipiron+3558"
    URL = "https://www.flipkart.com/search?q=" + keyword_string

     
    browser = webdriver.Chrome(chrome_options=chrome_options)  
    browser.get(""+URL)
    search_soup = BeautifulSoup(browser.page_source)  


    type1 = search_soup.find_all('div', {"class":"_2-gKeQ"})
    #electronics
    if(len(type1)>0):
        count =0
        for item in type1:
            ele = {}
            print("___________________________________")
            count = count + 1
            print(item.find('div',{"class":"_3wU53n"}))
            ele['tag'] = str(item)
            ele['name'] = item.find('div',{"class":"_3wU53n"}).text
            print("\n")
            if( item.find('img',{"class":"_1Nyybr"}) is not None):
                if( 'src' in item.find('img',{"class":"_1Nyybr"})):
                    print(item.find('img',{"class":"_1Nyybr"})['src'])
                    ele['pic'] = item.find('img',{"class":"_1Nyybr"})['src']
                else:
                    print('Image Not  Available')
            else:
                    print('Image Not  Available')
            print("\n")
            print(item.find('a',{"class":"_1UoZlX"})['href'])
            ele['href'] = item.find('a',{"class":"_1UoZlX"})['href']
            print("\n")
            if(item.find('div',{"class":"_1vC4OE"}) is not None):
                ele['cost'] = item.find('div',{"class":"_1vC4OE"}).text
                print(item.find('div',{"class":"_1vC4OE"}).text)

            STUFF.append(ele)


                       

        print("Count:"+str(count))
        STUFFER()
        return STUFF 

    else:
        type2 = search_soup.find_all('div', {"class":"_3liAhj"})
        #hoodies
        if(len(type2)>0):
            count =0
            for item in type2:
                ele ={}
                print("___________________________________")
                count = count + 1
                print(item.find('a',{"class":"_2cLu-l"}).text)
                ele['name'] = item.find('a',{"class":"_2cLu-l"}).text
                print("\n")
                if( item.find('img',{"class":"_1Nyybr"}) is not None):
                    if( 'src' in item.find('img',{"class":"_1Nyybr"})):
                        ele['pic'] = item.find('img',{"class":"_1Nyybr"})['src']
                    else:
                        print("Image Not available")
                else:
                    print('Image Not  Available')
                print("\n")

                ele['href'] = item.find('a',{"class":"_2cLu-l"})['href']
                print(item.find('a',{"class":"_2cLu-l"})['href'])
                print("\n")
                if(item.find('div',{"class":"_1vC4OE"}) is not None):
                    ele['cost'] = item.find('div',{"class":"_1vC4OE"}).text
                    print(item.find('div',{"class":"_1vC4OE"}).text)

                STUFF.append(ele)

            print("Count:"+str(count))
            #STUFFER()
            return STUFF

'''
def STUFFER():
    global STUFF
 
    listo =randy()
    x =0
    for item in STUFF:
        if(x > (len(listo) - 1) ):
            break
        STUFF[x]['pic'] = listo[x]
        x = x + 1

        
def randy():
    return ["https://rukminim1.flixcart.com/image/312/312/computer/p/y/h/dell-inspiron-15-notebook-original-imaemggfk6zmxxg3.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/d/g/h/dell-inspiron-15-notebook-original-imaeh5uyqgzfzefr.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/u/v/2/dell-inspiron-notebook-original-imaefnkyxrkypytv.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/h/e/m/dell-inspiron-15-notebook-original-imaege4hydsbvrf5.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/r/u/f/dell-inspiron-notebook-original-imaemgkz63tafsxq.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/d/g/h/dell-inspiron-15-notebook-original-imaepc5xymgcm2zs.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/r/u/f/dell-inspiron-notebook-original-imaemxamvrdqze2q.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/computer/3/9/e/dell-inspiron-notebook-original-imaemgnzhuj9qsat.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/mouse/2/t/m/dell-ms-116-original-imaekh9yeev9qsdr.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/keyboard/gaming-keyboard/e/y/q/dell-kb-216-original-imaeh65g7s5tw3vn.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/keyboard/laptop-keyboard/u/u/g/dell-multimedia-kb216-original-imaeh5x55baa4veu.jpeg?q=70",
            "https://rukminim1.flixcart.com/image/312/312/mouse/p/x/a/dell-ms111-3-button-wired-original-imaeenhxjscqkay6.jpeg?q=70"]
'''
