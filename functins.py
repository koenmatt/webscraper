import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import datetime


Data_Source = ['https://www.nasdaq.com/news-and-insights/topic/companies/dividends/page/2'
               'https://www.marketbeat.com/headlines/all/3/'
               ''
               ''
               '']


def generate_dates(days):
    """Generate dates to use in URL for however many days back you want"""
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(days)]
    test_dates = []
    for i in date_list:
        x = i.strftime('%m-%d-%Y')
        test_dates.append(x)
    return test_dates

def generate_urls(first_page, last_page):

    """Returns a list of urls from which to scrape headline data, from first page in the range
    to last page in the range"""

    urls = []
    for i in range(first_page, last_page):
        url = 'https://seekingalpha.com/market-news/{}'.format(i)
        urls.append(url)
    return urls

def extract_raw_html_data(first_page, last_page):

    """Returns a list of raw html data from each page, for each headline box
    (includes ticker info, date/time, headline), will clean in future function

     Note: Will have to change headers every couple months"""

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/88.0.4324.150 Safari/537.36'}
    html_data = []
    k = 0
    for url in generate_urls(first_page, last_page):
        time.sleep(5)
        session = requests.Session()
        response = session.get(url, headers = headers)
        print(response)
        k += 1
        print(k)
        soup = BeautifulSoup(response.content,"html.parser")
        html = soup.find_all('li', class_= 'item')
        html_data.append(html)

    return html_data


def extract_headline_data(first_page,last_page):
    """Returns a dataframe including date/time, company tickers, and headline given what pages
    (timeframe) and company name. Ensure that the difference between first/last page is less than 200
    otherwise it glitches/takes too long"""

    print('Your web-scraper will take approximately',(last_page - first_page)*7 / 60, 'Minutes to complete')
    headlines_tickers_raw = []
    times_series = []
    for data_parts in extract_raw_html_data(first_page,last_page):
        for data in data_parts:
            media_left = data.find('div', class_='tiny-share-widget')
            if media_left is None:
                pass
            else:
                headline = media_left['data-tweet']
                headlines_tickers_raw.append(headline)
                date = data.find('span', class_='item-date')
                times_series.append(date.string)

    return pd.DataFrame({'Time/Date': times_series, 'Headline_Ticker_Raw': headlines_tickers_raw})


