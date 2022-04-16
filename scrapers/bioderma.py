from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\bioderma.csv'

data = []

urlBase = 'https://www.bioderma.eg'

driver = webdriver.Firefox()
links = [ '/hygiene', '/skincare', '/suncare']

for category_link in links:
    print(category_link[1:])
    driver.get(urlBase + category_link)
    time.sleep(4)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')

    products = soup.find('div', class_='product-list-results').div.find_all('div', recursive=False)
    print(len(products))
    for product in products:
        name = product.div.find('div', class_='content').find('h2', class_='title-1--product').text.strip()
        print(name)
        img_link = urlBase + product.find('img')['src']
        print(img_link)
        skins = []
        skins_container = product.find('p', class_='skin').find_all('span')
        for skin in skins_container:
            skins.append(skin.text.strip())
            # print(skin)
        print(skins)
        link = urlBase + product.find('div', class_='content').a.get('href')
        print(link)
        driver.get(link)
        time.sleep(3)
        item_soup = BeautifulSoup(driver.page_source, 'lxml')
        description = item_soup.find('h2', attrs={'itemprop':'description'}).text.strip()
        features = []
        features_container1 = item_soup.find('div', id='benefice').find_all(text=True, recursive=False)
        for feature in features_container1:
            if not feature.strip():
                continue
            features.append(feature.strip())
        features_container2 = item_soup.find('div', id='benefice').find_all('li')
        for feature in features_container2:
            features.append(feature.text.strip())
        print(description)
        print('features')
        for feature in features:
            print('\t' + feature.strip())
        data.append([category_link[1:], name, '; '.join(skins), description, '; '.join(features), img_link, link])

driver.quit()

with open(sub_directory_name, 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['category', 'name','skins','description', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)