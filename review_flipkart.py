import requests
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from selenium import webdriver
from bs4 import BeautifulSoup

analyzer = SentimentIntensityAnalyzer()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
proxies = {'https': random.choice(proxies_list)}

def flipkartreviews(url):

    #PROXY = "52.69.175.99:3128"#""+random.choice(proxies_list) # IP:PORT or HOST:PORT
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)


    pageNum = 1
    count =0

    STUB =[]
    while True:
       if(pageNum>3):
          break
       browser = webdriver.Chrome(chrome_options=chrome_options) #'S:\MAIN_PROJECT\flipkart\chromedriver.exe')
       browser.get(""+url+"&page="+str(pageNum))
       search_soup = BeautifulSoup(browser.page_source) #,"lxml")
       #print(search_soup.prettify())


       for rev in search_soup.find_all("div",{"class":"_3DCdKt"}):
          print("______________________________________________________")
          stuff = rev.find("div",{"class":"qwjRop"}).text   
          print(stuff)
          item ={}

          item['review'] = stuff[:200]
          #STUB.append(stuff)
          if(True):
                sentimenta = analyzer.polarity_scores(str(stuff))
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
                STUB.append(item)

          
          count = count + 1
          print("______________________________________________________")

       pageNum = pageNum + 1
       browser.quit()

    
    print("______________________________________________________")
    print("count for 3 pages is "+str(count))
    print("______________________________________________________")
    return STUB



   

