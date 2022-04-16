from itertools import product
from unicodedata import category
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv

data = []

urlBase = 'https://www.bobbibrowncosmetics.com'

driver = webdriver.Firefox()
links = [ '/products/13994/makeup/face', '/products/2339/makeup/lips', '/products/2326/makeup/eyes', '/products/23824/makeup/face/cheeks', '/products/14006/skincare']


for category_link in links:
    subcategory = category_link.split('/')[len(category_link.split('/')) - 1]
    category = ''
    if subcategory is not 'skincare':
        category = 'makeup'
    else:
        category = 'skincare'
    print(category)
    print(subcategory)
    driver.get(urlBase + category_link)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    products = soup.find('div', attrs={'role':'list'}).find_all('div', recursive=False)
    i = 0
    for item in products:
        if not item.find('div', class_='product-brief'):
            continue
        i += 1
        print(i)
        name = item.find('h3', class_='product-brief__header').text.strip()
        print(name)
        price = item.find('span', class_='price').text.strip()
        print(price)
        img_link = urlBase + item.find('div', class_='product-brief__image-wrapper').find('img').get('data-src')
        print(img_link)
        link = urlBase + item.find('a', class_='product-brief__headline-link').get('href')
        print(link)
        colors = []
        colors_container = item.find('div', class_='product-brief__shades')
        if colors_container is not None:
            colors_container = colors_container.find('div', class_='product-brief-shades__grid').div.div.find_all('div', recursive=False)
            for color in colors_container:
                colors.append(color.a['title'])
        print(colors)
        driver.get(link)
        time.sleep(5)
        item_soup = BeautifulSoup(driver.page_source, 'lxml')
        description = item_soup.find('div', id='what')
        if description is not None:
            description = description.text.strip()
        else:
            description = 'NA'
        print(description)
        features = item_soup.find('div', id='why')
        if features is not None:
            features = features.text.strip()
        else:
            features = 'NA'
        print(features)
        skins = item_soup.find('div', id='who')
        if skins is not None:
            skins = skins.text.strip()
        else:
            skins = 'NA'
        print(skins)
        data.append([name, price, skins, '; '.join(colors), description, features, img_link, link])
    

driver.quit()
    
with open('bobbibrown.csv', 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['name', 'price', 'skins', 'colors', 'description', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)