from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\becca.csv'

urlBase = 'https://www.amazon.com'

data = []

driver = webdriver.Firefox()

driver.get('https://www.amazon.com/s?srs=17716759011')

time.sleep(2)

html_text = driver.page_source

soup = BeautifulSoup(html_text, 'lxml')

all_items = soup.find_all('div', attrs={'data-index': True, 'data-uuid': True})

for item in all_items:
    img_link = item.find('img')['src']
    print(img_link)
    link = item.find('h2').find('a').get('href')
    driver.get(urlBase + link)
    time.sleep(2)
    sub_html_text = driver.page_source
    sub_soup = BeautifulSoup(sub_html_text, 'lxml')
    name = sub_soup.find('span', id="productTitle").text.strip()
    print(name)
    price = sub_soup.find('div', id='corePrice_desktop').find('tr')
    if price is not None:
        price = price.find_all('td')[1].find('span').find('span').text
    else:
        price = 'NA'
    print(price)
    final_description = ''
    description = sub_soup.find('div', id="productDescription").text.strip()
    if not description:
        description = 'NA'
    features = ''
    description_features = sub_soup.find('div', id='feature-bullets').find('ul')
    if description_features is not None:
        description_features = description_features.find_all('li')
        for feature in description_features:
            if '$' in feature.text or 'price' in feature.text or 'Price' in feature.text:
                continue
            features += '-\t' + feature.text.strip() + '\n'
    if not features:
        features = 'NA'
    data.append([name, price, description, features, img_link, urlBase + link])
    

driver.quit()
with open(sub_directory_name, 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['name', 'price', 'desciption', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)