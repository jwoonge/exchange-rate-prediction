import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
nltk.download('wordnet')
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import csv
import os

def read_exchange_rate_csv(dir):
    ret = []
    count = 0
    currency = []
    with open(dir, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            tmp = row[0].split(',')
            if count>0:
                floattmp = []
                for val in tmp:
                    floattmp.append(float(val))
                ret.append(floattmp)
            else:
                currency = tmp
            count += 1
    return ret, currency

def read_news(dir, exchange_rates):
    X = []; Y=[]
    news_dir = dir
    for country in os.listdir(news_dir):
        print(country)
        for week in os.listdir(news_dir+'/'+country):
            y = exchange_rates[int(week)][currencies.index(country)]
            article = ""
            for docs in os.listdir(news_dir+'/'+country+'/'+week):
                try:
                    f = open(news_dir+'/'+country+'/'+week+'/'+docs, 'r', encoding='utf-8')
                    article += f.read()
                except:
                    print('except')
                    pass
            X.append(article)
            Y.append(y)
    return X, Y

exchange_rates, currencies = read_exchange_rate_csv('exchangerates/exchangeRateMatrix.csv')
X, Y = read_news('news/',exchange_rates)
print(len(X), len(Y))

