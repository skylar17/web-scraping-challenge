# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "Resources/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}


    # NASA Mars News
    mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[1].text

    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p


    # JPL Mars Space Images - Featured Image
    jpl_main_url = "https://www.jpl.nasa.gov"
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    path = jpl_soup.find('div', class_="carousel_items").article['style']
    full_length_path = len(path)
    x = len("background-image: url('")
    y = full_length_path - len("');")
    image_path = jpl_soup.find('div', class_="carousel_items").article['style'][x:y]
    
    mars_dict["featured_image_url"] = jpl_main_url + image_path

    # Mars Facts
    Facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(Facts_url)

    df = tables[2]
    df.columns = ['Description', 'Mars']

    # converting to dict
    data_dict = df.to_dict(orient='records')
    mars_dict["mars_facts"] = data_dict
    

    # Mars Hemispheres
    main_url = "https://astrogeology.usgs.gov/"
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemis_url)
    hemis_html = browser.html
    hemis_soup = bs(hemis_html, 'html.parser')

    hemis_home = hemis_soup.find('div', class_='collapsible results')
    all_hemis = hemis_home.find_all('div', class_='item')

    hemis_image_urls = []

    # Iterate through all four hemisphere boxes
    for each in all_hemis:
        
        hemisphere = each.find('div', class_="description")
        
        title = hemisphere.h3.text
        hemi_link = hemisphere.a["href"]  
        
        browser.visit(main_url + hemi_link)
        
        each_hemi_html = browser.html
        each_soup = bs(each_hemi_html, 'html.parser')
        
        img_url = each_soup.find('img', class_="wide-image")['src']
        
        
        url_dict = {}
        url_dict["title"] = title
        url_dict["img_url"] = img_url
        
        hemis_image_urls.append(url_dict)

        mars_dict["hemisphere_image_urls"] = hemis_image_urls


    return mars_dict
    
