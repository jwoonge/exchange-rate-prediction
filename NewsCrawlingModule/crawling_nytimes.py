import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def findStartAndEndDate(lastEndDate) :
    dateNum = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    startYear  = int(lastEndDate[0])
    startMonth = int(lastEndDate[1])
    startDate  = int(lastEndDate[2]) + 1
    if startDate > dateNum[startMonth - 1] :
        startDate = startDate -  dateNum[startMonth - 1]
        startMonth += 1
        if startMonth > 12 :
            startMonth = 1
            startYear += 1  
    endYear = startYear
    endMonth = startMonth
    endDate = startDate + 6
    if endDate > dateNum[endMonth - 1] :
        endDate = endDate - dateNum[endMonth - 1]
        endMonth += 1
        if endMonth > 12 :
            endMonth = 1
            endYear += 1
            
    strStartYear  = str(startYear)
    strStartMonth = str(startMonth)
    strStartDate  = str(startDate)
    if int(startMonth / 10) <1 :
        strStartMonth = "0" + strStartMonth
    if int(startDate / 10) <1 :
        strStartDate = "0" +strStartDate
    strStarDateList=  [strStartYear,strStartMonth,strStartDate] 
    
    strEndYear  = str(endYear)
    strEndMonth = str(endMonth)
    strEndDate  = str(endDate)
    if endMonth / 10 <1 :
        strEndMonth = "0" + strEndMonth
    if endDate / 10 <1 :
        strEndDate = "0" +strEndDate
    strEndDateList=  [strEndYear,strEndMonth,strEndDate]
    return strStarDateList, strEndDateList
def date_to_week_list() :
    initYear = "2016"
    initMonth = "12" 
    initDate = "31"
    lastEndDate = [initYear,initMonth,initDate]
    date_to_week_list = []
    cnt = 0
    while True :
        s,e = findStartAndEndDate(lastEndDate) 
        date_to_week_list.append([s,e])
        lastEndDate = e
        cnt += 1
        if cnt == 150 :
            break
    return date_to_week_list


def crawling_nytimes(currency, country_names, direct, driver):
    date_to_week = date_to_week_list()
    todo_list = dict()
    base_url = "http://www.nytimes.com"
    sections = r'&sections=World%7Cnyt%3A%2F%2Fsection%2F70e865b6-cc70-5181-84c9-8368b3a5c34b&sort=best&startDate='

    for country_name in country_names:
        print('  for search keyword ',country_name)
        for week in range(0,150): #150
            print('\tweek',week)
            start_date = date_to_week[week][0][0]+date_to_week[week][0][1]+date_to_week[week][0][2]
            end_date = date_to_week[week][1][0]+date_to_week[week][1][1]+date_to_week[week][1][2]
            url = base_url + '/search?dropmap=true&endDate='+end_date+'&query='+country_name + sections + start_date+'&types=article'

            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            el = soup.select('div.css-e1lvw9')
            
            for i in range(len(el)):
                title = el[i].select('h4.css-2fgx4k')[0].text
                url = el[i].select('a')[0]['href']
                if not todo_list.get(url):
                    todo_list[url] = [week, title]

    print('\n  got ',len(todo_list.keys()),'urls')
    print('  crawling article bodies...')

    try:
        f = open('resource/urls/'+currency+'.txt', 'a', encoding='utf-8')
        for url in todo_list.keys():
            title = todo_list[url][1].replace(':',' ')
            date = todo_list[url][0]
           
            f.write(url+'##'+str(date)+'##'+title+'\n')
        f.close()

    except:
        print('error!!!!!')


    count = 0
    for url in todo_list.keys():
        body = crawling_nytimes_body(base_url + url, driver)
        title = todo_list[url][1].replace(":"," ")
        date = todo_list[url][0]
        directory = direct + '/' +currency+'/'+str(date)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #file_name = directory+'/'+title+'.txt'
        try:
            f = open(directory+'/times'+str(count)+'.txt', 'w', encoding='utf-8')
            f.write(title+'\n')
            f.write(body)
        except:
            print('error!')
        finally:
            f.close()
        count += 1
            
def crawling_nytimes_body(url, driver):
    driver.get(url)
    driver.implicitly_wait(3)
    #driver.find_element_by_xpath('//button[@data-testid="search-show-more-button"]').click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    el = soup.select('p.css-158dogj.evys1bk0')
    body = ""
    for i in range(len(el)):
        body += el[i].text + '\n'
    return body
    
def login_nytimes(driver):
    try:
        driver.get(r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fmultiproduct%2Flp8KQUS.html%3FcampaignId%3D7QQFH%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead')
        driver.find_element_by_xpath('//*[@id="js-google-oauth-login"]').click()


    except:
        return

def click_show_more_btn(driver):
    while(True):
        try:
            wait = WebDriverWait(driver,10)
            #driver.find_element_by_xpath('//button[@data-testid="search-show-more-button"]').click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="search-show-more-button"]')))
            element.click()
        except:
            break

if __name__=='__main__':

    options = webdriver.ChromeOptions()
    #options.headless=True
    driver = webdriver.Chrome('C:\\Users\\jwoonge\\Desktop\\selenium\\chromedriver_win32\\chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    login_nytimes(driver)
    crawling_nytimes('china', ['china'], '../news', driver)
