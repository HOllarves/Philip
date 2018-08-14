# import tweepy library for twitter api access and textblob libary for sentiment analysis
import csv
import numpy as np
from textblob import TextBlob
import datetime
import time
import requests
import json

def main():

    # set path of csv file to save sentiment stats
    path = '../live_reddit_15m.csv'
    f = open(path,"a")
    url = 'https://www.reddit.com/r/bitcoin/.json'
    hdr = {'User-Agent': 'windows:r/bitcoin.single.result:v1.0' + '(by /u/)'}
    f1 = open('../reddit_data_15m','a')
    # access twitter api via tweepy methods
    while True:

        try:
            # fetch tweets by keywords
            titles = []
            req = requests.get(url, headers=hdr)
            json_data = json.loads(req.text)


            for post in json_data['data']['children']:
                titles.append(post['data']['title'])
            # get polarity
            polarity = get_polarity(titles,f1)
            sentiment = np.mean(polarity)

            # save sentiment data to csv file
            f.write(str(sentiment))
            f.write(","+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
            f.write("\n")
            f.flush()
            print("Success!")
            time.sleep(900)
        except Exception as x:
            print("Error!")
            print(x)
            print("Retrying in 60 seconds")
            time.sleep(60)
    

def get_polarity(headlines,f):
    # run polarity analysis on headlines
    reddit_polarity = []
    for title in headlines:
        f.write(title+'\n')
        analysis = TextBlob(title)
        reddit_polarity.append(analysis.sentiment.polarity)

    return reddit_polarity

main()
