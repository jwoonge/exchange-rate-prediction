import requests
from bs4 import BeautifulSoup
import os
from crawling_nytimes import date_to_week_list

def month_table(input_str):
    if input_str=='Jen':
        return 1
    elif input_str=='Feb':
        return 2
    elif input_str=='Mar':
        return 3
    elif input_str=='Apr':
        return 4
    elif input_str=='May':
        return 5
    elif input_str=='Jun':
        return 6
    elif input_str=='Jul':
        return 7
    elif input_str=='Aug':
        return 8
    elif input_str=='Sep':
        return 9
    elif input_str=='Oct':
        return 10
    elif input_str=='Nov':
        return 11
    elif input_str=='Dec':
        return 12
    else:
        return 0

def str_to_week_num(input_str):
    week_LUT = date_to_week_list()

    tmp = input_str.split(' ')
    print(tmp)
    if 'h' in tmp[1]:
        return -1
    month = month_table(tmp[1])
    day = int(tmp[2].replace(',',""))
    year = int(tmp[3])
    int_date = day + month*100 + year*10000
    
    week = -1
    for i in range(len(week_LUT)):
        int_start = 10000*int(week_LUT[i][0][0]) + 100*int(week_LUT[i][0][1]) + int(week_LUT[i][0][2])
        int_end = 10000*int(week_LUT[i][1][0]) + 100*int(week_LUT[i][1][1]) + int(week_LUT[i][1][2])
        if int_start <= int_date and int_end >= int_date :
            week = i

    return week


def crawling_nydailynews(currency, country_names, direct):
    todo_list = dict()
    base_url = 'http://nydailynews.com'

    for country_name in country_names:
        print('  for search keyword ',country_name)
        url = base_url + '/search/' + country_name + '/170-w/ALL/date/1/'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        num_article = soup.select('h2.tag.flex-1-col.spaced.spaced-right.spaced-md.number-results')[0].text.split(' ')[0]
        num_article = int(num_article.replace(",",""))
        last_page = int(num_article/12)+1
        print('\tfound ',num_article,'articles')
        print('\tlast_page:',last_page)
        
        for page in range(1, last_page+1):
            url = 'http://www.nydailynews.com/search/' + country_name + '/170-w/ALL/date/' + str(page) + '/'
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            el = soup.select('li.col.col-desktop-3.col-tablet-3.col-mobile-6')
            article_num = len(el)
            for i in range(article_num):
                date = el[i].select('span.timestamp')[0].text
                
                if date in range(0,150):
                    title = el[i].select('a.no-u')[0].text
                    url = el[i].select('a.no-u')[0]['href']
                    if not todo_list.get(url):
                        todo_list[url] = [date, title]
    
    print('  got ',len(todo_list.keys()),'urls')
    print('  crawling article bodies...')
    for url in todo_list.keys():
        body = crawling_nydailynews_body(base_url + url)
        title = todo_list[url][1].replace(":"," ")
        date = todo_list[url][0]
        directory = direct + '/' +currency+'/'+str(date)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = directory+'/'+title+'.txt'
        try:
            f = open(file_name, 'w', encoding='utf-8')
            f.write(body)
        except:
            print('error!')
        finally:
            f.close()
    

def crawling_nydailynews_body(url):
    print(url)
    ret = ""
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    body = soup.select('div[data-pb-name="Article Body (Elements)"]')[0].select('div[data-type="text"]')
    for i in range(len(body)):
        ret += body[i].text + "\n"
    return ret

if __name__=='__main__':
    crawling_nydailynews('korea', ['korea'], '../news')