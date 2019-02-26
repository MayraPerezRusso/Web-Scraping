from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    url1 = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(url1)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='content_title')
    results2 = soup.find_all(class_='rollover_description_inner')
    news_title=results[0].text
    news_p=results2[0].text


    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    x=soup.find_all("a", class_='fancybox')
    featured_image_url1=[]
    for i in x:
        featured_image_url1.append(i['data-fancybox-href'])
    featured_image_url='https://www.jpl.nasa.gov'+featured_image_url1[0]
    

    url3='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'lxml')
    mars_weather1 = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather_last=mars_weather1[2].text.strip()
    mars_weather_last=mars_weather_last.replace("\n",". ")
    mars_weather=mars_weather_last[:mars_weather_last.rfind("pic")]
    

    url3='https://space-facts.com/mars/'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'lxml')
    title_fact=soup.find_all('td',class_='column-1')
    fact=soup.find_all('td',class_='column-2')
    title=[]
    value=[]
    for item in range(len(title_fact)-1):
        title.append(title_fact[item].strong.text.strip())
        value.append(fact[item].text.strip())
    table_fact=pd.DataFrame({'Information':title,
                            'value':value})
    table_fact=table_fact.set_index('Information')
    table_fact=table_fact.to_html(classes='table_fact.html')

    
    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url4)
    soup = BeautifulSoup(response.text, 'lxml')
    link=soup.find_all('a',class_='itemLink')
    list_link=[]
    for l in range(len(link)):
        list_link.append('https://astrogeology.usgs.gov'+link[l]['href'])
    name=[]
    link_img=[]

    for i in range(len(list_link)):
        browser.visit(list_link[i])
        browser.click_link_by_partial_text('Open')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_link=soup.find_all('img', class_='wide-image')
        name_img=soup.find_all('h2', class_='title')
        name.append(name_img[0].text)
        link_img.append('https://astrogeology.usgs.gov'+img_link[0]['src'])
    images={'title': name,
            'img_url':link_img}

    mars_data={'news_title':news_title,
     'news_p':news_p,
     'featured_image_url':featured_image_url,
     'mars_weather':mars_weather,
     'table_fact':table_fact,
     'images_url':images}

    browser.quit()
    return mars_data