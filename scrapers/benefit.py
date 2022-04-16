from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\benefit.csv'

urlBase = 'https://www.benefitcosmetics.com'

items_link = []
items_img = []
data = []

driver = webdriver.Firefox()

driver.get('https://www.benefitcosmetics.com/en-us/all-makeup')

time.sleep(2)



while True:
    text_html = driver.page_source
    soup = BeautifulSoup(text_html, 'lxml')
    items = soup.find('div', class_='search-list__container').find_all('div', class_='card')
    for item in items:
        items_img.append(urlBase + item.find('img')['src'])
        items_link.append(urlBase + item.a.get('href'))
    next_page_btn = soup.find(class_='pagination__link-right')
    if not next_page_btn:
        break
    driver.execute_script('document.querySelector(".pagination__link-right").click()')
    time.sleep(2.5)

for i, link in enumerate(items_link):
    driver.get(link)
    time.sleep(2)
    html_item_text = driver.page_source
    soup_item = BeautifulSoup(html_item_text, 'lxml')
    name = soup_item.find('h1', class_='product-title')
    if not name:
        continue
    name = name.text.strip()
    print(name)
    price = soup_item.find('div', class_='price__wrapper').find('div', class_='price').find('span')
    if not price:
        price = 'NA'
    else:
        price = price.find(text=True, recursive=False)
    print(price)
    colors = []
    shades = soup_item.find('div', class_='shades')
    if shades is not None:
        colors_container = shades.find('ul').find_all('li')
        for color_container in colors_container:
            color = color_container.find('button').attrs['aria-label']
            colors.append(color)
            print(color)
    if len(colors) == 0:
        colors = 'NA'
    features = ''
    features_container = soup_item.find('div', class_='bullet-list product-info__section')
    if features_container is not None:
        features_container = features_container.find('ul').find_all('li')
        for feature_container in features_container:
            features += '-\t' + feature_container.text.strip() + '\n'
    else:
        features = 'NA'
    print(features)
    description = soup_item.find('div',id='ac-0').div.div.text.strip()
    if not description:
        description = 'NA'
    print(description)
    print(link)
    print(items_img[i])
    data.append([name, price,';'.join(colors), description, features, items_img[i], link])

driver.quit()

with open(sub_directory_name, 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['name', 'price','colors', 'description', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)