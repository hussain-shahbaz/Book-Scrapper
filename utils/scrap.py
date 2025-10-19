from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time,sleep
import threading
#SCRAPE STATE
from .ScraperState import ScraperState,ScraperStatus

#CONFIGURE SETTINGS
chrome_options = Options()
def setOptions():
    chrome_options.add_argument("--headless=new")                 
    chrome_options.add_argument("--disable-gpu")                  
    chrome_options.add_argument("--no-sandbox")                    
    chrome_options.add_argument("--disable-dev-shm-usage")        
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_argument("--disable-infobars")            
    chrome_options.add_argument("--disable-extensions")          
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.page_load_strategy = 'eager'                   
setOptions()
driver = webdriver.Chrome(options=chrome_options)
filePath = 'books.csv'
## DATAFRAME
def load_existing_data():
    try:
        curr = pd.read_csv(f'data\\{filePath}')
        if len(curr) > 0:
            return curr.fillna('').astype(str)
    except:
        pass
    return pd.DataFrame(columns=['Sr.No','Title', 'By', 'Description','Rating', 'Date', 'Publisher', 'Language', 'Pages','Want to Read','Have Read','Currently Reading','ISBN'])

df = load_existing_data()

## ENV VARIABLES
BASE_URL = 'https://openlibrary.org'
MAX_PAGES = 1313
START_PAGE = min(len(df) // 20,MAX_PAGES)



## SCRAPER STATE
state = ScraperState(MAX_PAGES)
state.setCurrentPage(START_PAGE)

## DATA SCRAPING
def ExtractBooksData(soup:BeautifulSoup, df:pd.DataFrame):
    count = len(soup.find_all('li', attrs={'class': 'searchResultItem'}))
    for div in soup.find_all('li', attrs={'class': 'searchResultItem'}):

        while state.status == ScraperStatus.PAUSED:
            print(state.status == ScraperStatus.PAUSED)  
            sleep(1) 
        
        book = div.find('div', attrs={'class': 'sri__main'})
        if not book:
            continue

        aTag = book.find('a', attrs={'class': 'results'})
        if not aTag or not aTag.has_attr('href'):
            continue

        detailUrl = aTag['href']
        driver.get(BASE_URL + detailUrl)
        detailSoup = BeautifulSoup(driver.page_source, 'html.parser')

        titleTag = detailSoup.find('h1', attrs={'class': 'work-title'})
        title = titleTag.get_text() if titleTag else ""

        byTag = detailSoup.find('a', attrs={'itemprop': 'author'})
        by = byTag.get_text() if byTag else ""

        ratingTag = detailSoup.find('span', attrs={'itemprop': 'ratingValue'})
        rating = ratingTag.get_text().split(' ')[0] if ratingTag and ratingTag.get_text() else ""

        statsList = detailSoup.find('ul', attrs={'itemprop': 'aggregateRating'})
        stats = statsList.find_all('li', attrs={'class': 'reading-log-stat'}) if statsList else []

        wantToRead = stats[0].find('span').get_text() if len(stats) > 0 and stats[0].find('span') else ""
        currReading = stats[1].find('span').get_text() if len(stats) > 1 and stats[1].find('span') else ""
        haveRead = stats[2].find('span').get_text() if len(stats) > 2 and stats[2].find('span') else ""

        descDiv = detailSoup.find('div', attrs={'class': 'read-more__content markdown-content'})
        descPara = descDiv.find('p') if descDiv else None
        description = descPara.get_text().rstrip() if descPara else ""
        
        pubDiv = detailSoup.find('div', attrs={'class': 'edition-omniline'})
        pub = pubDiv.find_all('div', attrs={'class': 'edition-omniline-item'}) if pubDiv else []

        date = publisher = language = pages = ""

        for item in pub:
            if item.find('span', attrs={'itemprop': 'datePublished'}):
                span = item.find('span', attrs={'itemprop': 'datePublished'})
                date = span.get_text() if span else ""
            elif item.find('a', attrs={'itemprop': 'publisher'}):
                span = item.find('a', attrs={'itemprop': 'publisher'})
                publisher = span.get_text() if span else ""
            elif item.find('span', attrs={'itemprop': 'inLanguage'}):
                span = item.find('span', attrs={'itemprop': 'inLanguage'})
                language = span.get_text() if span else ""
            elif item.find('span', attrs={'itemprop': 'numberOfPages'}):
                span = item.find('span', attrs={'itemprop': 'numberOfPages'})
                pages = span.get_text() if span else ""
        
        isbnDiv = detailSoup.find('dd',attrs={'itemprop':'isbn'})
        isbn = isbnDiv.get_text().strip().strip().rstrip() if (isbnDiv and isbnDiv.get_text() != "") else ""

        new_entry = {
            'Sr.No': str(len(df)),
            'Title': title,
            'By': by,
            'Rating': rating,
            'Date': date,
            'Publisher': publisher,
            'Language': language,
            'Pages': pages,
            'Want to Read': wantToRead,
            'Have Read': haveRead,
            'Currently Reading': currReading,
            'Description': description,
            'ISBN':isbn
        }
        state.addBooks(1)
        df.loc[len(df)] = new_entry
        pd.DataFrame([new_entry]).to_csv(f'data\\{filePath}', mode='a', header=False, index=False)
    return count

def ScrapeData():
    state.start()
    try:
        for i in range(START_PAGE, MAX_PAGES + 1):
            if state.status == ScraperStatus.STOPPED:
                return
            if(START_PAGE >= MAX_PAGES):
                state.setCompleted()
                return

            state.setCurrentPage(i)
            start = time()
            url = f'''{BASE_URL}/search?q=subject_key%3A"literature"&mode=everything&language=eng&page={i}'''
            try:


                driver.get(url)
                soup = BeautifulSoup(driver.page_source,features='html.parser')
                count = ExtractBooksData(soup, df)
                
                stop = time()
                elapsed_time = stop - start
                
                print(state.getStatus())
            except Exception as e:
                continue
        
        state.stop()
    except Exception as e:
        state.stop()   
        
