from bs4 import BeautifulSoup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
from datetime import datetime

class scraping():
    def __init__(self):
        pass

    def scrape(self):
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        url = 'https://redplanetscience.com/'
        browser.visit(url)

        for x in range(1):
    
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
    
            results = soup.find('div', class_= 'list_text')
    
            latest_title = results.find('div', class_= 'content_title').text
            latest_paragraph = results.find('div', class_= 'article_teaser_body').text

        image_url = 'https://spaceimages-mars.com/'
        browser.visit(image_url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        picture = soup.find('div', class_='header')
        image_feat = picture.find('img', class_='headerimage fade-in')['src']

        featured_image_url = url+image_feat

        url = 'https://galaxyfacts-mars.com/'
        table = pd.read_html(url)

        mars_df = table[0]
        mars_df = mars_df.iloc[1: , :]

        mars_df.rename(columns = {list(mars_df)[0]: 'Comparison'}, inplace = True)
        mars_df.rename(columns = {list(mars_df)[1]: 'Mars'}, inplace = True)
        mars_df.rename(columns = {list(mars_df)[2]: 'Earth'}, inplace = True)
        mars_df.set_index(mars_df['Comparison'], drop=True)

        data_html = mars_df.to_html(header=True)

        image_route_list = ['cerberus.html','schiaparelli.html','syrtis.html','valles.html']
        hemisphere_title_list = []
        image_url_list = []

        for image_route in image_route_list:
            url = f"https://marshemispheres.com/{image_route}"
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')
    
            results = soup.find('div', class_='downloads')
            more_results = soup.find('div', class_='cover')
    
            for x in range(1):
                image_url = results.find('img', class_='thumb')['src']
                hemisphere = more_results.find('h2', class_='title').text
            
                image_url_list.append(url+'/'+image_url)
                hemisphere_title_list.append(hemisphere)

        hemisphere_list = []
        for hemi in hemisphere_title_list:
            hemi_title = hemi.replace(' Enhanced','')
            hemisphere_list.append(hemi_title)

        hemisphere_dict = {'title': hemisphere_list,'img_url':image_url_list}

        browser.quit()

        final_data = {
            "news_title": latest_title,
            "news_paragraph": latest_paragraph,
            "featured_image_url": featured_image_url,
            "mars_facts": data_html,
            "hemispheres": hemisphere_dict,
            "last_updated": datetime.utcnow()
        }
        return(final_data)