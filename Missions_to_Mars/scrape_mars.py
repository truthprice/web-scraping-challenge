# Dependencies
import pandas as pd
import pymongo

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    martianary = {}
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = "https://redplanetscience.com/"
    browser.visit(url)
    
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    news_title = soup.find_all('div', class_="content_title")[0].text
    news_p =  soup.find_all('div', class_="article_teaser_body")[0].text

    martianary['news_title'] = news_title
    martianary['news_p'] = news_p
    
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    results = soup.find_all('div', class_='floating_text_area')
    for result in results:       
        image_url = result.a['href']

            
    featured_image_url = url + image_url

    martianary['featured_image_url'] = featured_image_url
    
    url = "https://galaxyfacts-mars.com"
    table = pd.read_html(url)
    table_df = table[1]
    table_df.columns = ['Descriptor', 'Value']
    table_df.set_index('Descriptor')
    html_table = table_df.to_html()
    html_table = html_table.replace('\n', '')

    martianary['html_table'] = html_table
    
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    results2 = soup.find_all('div', class_='description')
    
    hem_url = []
    for result in results2:
        title = result.find('h3').text
        image_url2 = result.a['href']
        full_url = url + image_url2
        browser.visit(full_url)
        html = browser.html
        soup = bs(html, "html.parser")
        full_img = soup.find('img', class_="wide-image")
        link = full_img['src']
        img_url = url + link
        
        hem_url.append({"title": title, "img_url": img_url})

    martianary['hem_url'] = hem_url
    
    browser.quit()
    return (martianary)