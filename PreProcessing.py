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
from sklearn.decomposition import TruncatedSVD
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

def expand_contractions(x):
    LUT = {"ain't": "is not", "aren't": "are not", "can't": "can not", "can't've": "can not have", "'cause": "because", "could've": "could have", "couldn't": "could not", "couldn't've": "could not have", "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", "he'd": "he would", "he'd've": "he would have", "he'll": "he will", "he'll've": "he he will have", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is", "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have", "I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will", "i'll've": "i will have", "i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have", "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not", "mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have", "so's": "so as", "that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are", "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would", "y'all'd've": "you all would have", "y'all're": "you all are", "y'all've": "you all have", "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have"}
    p = re.compile('({})'.format('|'.join(LUT.keys())), flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = LUT.get(match)\
        if LUT.get(match)\
        else LUT.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_text = p.sub(expand_match, x)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def string_processing(X):
    stemmer = WordNetLemmatizer()
    for i in range(len(X)):
        x = re.sub(r'’', "'", X[i])
        x = re.sub(r'”', '"', x)
        x = re.sub(r'\\n', ' ', x)
        x = re.sub(r'\\\'', "'", x)
        x = expand_contractions(x)

        x = re.sub(r'[^a-zA-Z0-9\s]', ' ', x)
        x = re.sub(r'\s+[a-zA-Z]\s+', ' ', x)
        x = re.sub(r'\^[a-zA-Z]\s+', ' ', x)
        x = re.sub(r'\s+', ' ', x, flags=re.I)

        x = x.lower()
        x = x.split()
        x = [stemmer.lemmatize(word) for word in x]
        x = ' '.join(x)
        X[i] = x
    return X

def pre_processing(X):
    X = string_processing(X)

    stopword = stopwords.words('english')
    stopword.remove('no')
    stopword.remove('not')
    vectorizer = CountVectorizer(stop_words=stopword)
    X = vectorizer.fit_transform(X).toarray()
    print(X.shape)

    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()
    svd = TruncatedSVD(n_components=1500)
    X = svd.fit_transform(X)

    return X



exchange_rates, currencies = read_exchange_rate_csv('exchangerates/exchangeRateMatrix.csv')
X, Y = read_news('news/',exchange_rates)
X = pre_processing(X)

