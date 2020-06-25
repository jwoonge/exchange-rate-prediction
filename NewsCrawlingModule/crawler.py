import os
from crawling_nydailynews import *
from crawling_nytimes import *


def get_countries(dir):
    countries = dict()
    f = open(dir, mode='r', encoding='utf-8')

    currency = ""
    for line in f:
        if line[0]=='@':
            currency = line[1:-1]
            #print(currency, end=' : ')
        else:
            if line[-2]=='/':
                line = line[:-1]
            country_name = line[:-1].split('/')
            print(country_name)
            countries[currency] = country_name

    return countries

if __name__=='__main__':
    countries = get_countries('resource/country.txt')
    
    options = webdriver.ChromeOptions()
    #options.headless=True
    driver = webdriver.Chrome('resource\\chromedriver_win32\\chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    login_nytimes(driver)

    for currency in countries.keys():
        print("crawling ",currency," from new-york times")
        crawling_nytimes(currency, countries[currency], '../news', driver)
    
    '''
    for currency in countries.keys():
        print("crawling ",currency," from new-york daily news")
        crawling_nydailynews(currency, countries[currency], '../news')
    '''
