from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\bhcosmetics.csv'

data = []

urlBase = 'https://www.bhcosmetics.com'

driver = webdriver.Firefox()
links = [ 'https://www.bhcosmetics.com/collections/eyes', 'https://www.bhcosmetics.com/collections/face', 'https://www.bhcosmetics.com/collections/lips','https://www.bhcosmetics.com/collections/brushes-and-tools' ]

for category_link in links:
    try:
        driver.get(category_link)
    except:
        print('too much time')

    time.sleep(10)

    

    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')

    products = soup.find_all('div', attrs={'aria-label': 'product'})
    i = 1
    for product in products:
        print('start')
        link = urlBase + product.find('a').get('href')
        print(i)
        print('link')
        name = product.find('h1').text.strip()
        print('name', name)
        price = product.find('div', class_='product-card__info-price').find('span').find(text=True, recursive=False).strip()
        print('price')
        try:
            driver.get(link)
        except:
            print('too much time')
        print('done loading')
        time.sleep(3)
        item_html_text = driver.page_source
        item_soup = BeautifulSoup(item_html_text, 'lxml')
        tabs = item_soup.find('div', class_='product-info').find('ul', attrs={'role': 'tablist'}).find_all('a')
        driver.execute_script("document.querySelectorAll('.product-info ul[role=tablist] a')[0].click()")
        description = item_soup.find('div', class_='product-info__content').find_all('div', recursive=False)[0].find_all('div', recursive=False)[1].text.strip()
        print('description')
        features = ''
        features_tab = item_soup.find(class_='product-info').find('ul', attrs={'role':'tablist'}).find_all('a')
        if len(features_tab) < 2:
            features = 'NA'
        else:
            driver.execute_script("document.querySelectorAll('.product-info ul[role=tablist] a')[1].click()")
            features = item_soup.find('div', class_='product-info__content').find_all('div', recursive=False)[1].find_all('div', recursive=False)[1].text.strip()
        print('features')
        img = item_soup.find('li', class_='slick-current').find('img')['src']
        print('img')
        data.append([name, price, description, features, img, link])
        print('done')
        i += 1

driver.quit()

with open(sub_directory_name, 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['name', 'price', 'description', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)


