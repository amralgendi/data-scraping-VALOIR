from cgitb import html
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\beesline.csv'

urlBase = 'https://www.eg.shopbeesline.com'

data = []

driver = webdriver.Firefox()

driver.get('https://www.eg.shopbeesline.com/en/products/view-all-products.html')


# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

driver.execute_script("document.querySelectorAll('.products.wrapper.grid.products-grid ol li')[document.querySelectorAll('.products.wrapper.grid.products-grid ol li').length - 1].scrollIntoView()")

time.sleep(2.5)

while True:
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    btn = soup.find('div', class_='products wrapper grid products-grid').find('ol').find('button', recursive=False)

    if btn is None:
        break
    print(btn)
    driver.execute_script("document.querySelector('.products.wrapper.grid.products-grid ol > button').click();")
    time.sleep(2.5)
    driver.execute_script("document.querySelectorAll('.products.wrapper.grid.products-grid ol li')[document.querySelectorAll('.products.wrapper.grid.products-grid ol li').length - 1].scrollIntoView()")
    time.sleep(1)

html_text = driver.page_source
soup = BeautifulSoup(html_text, 'lxml')
all_items = soup.find('div', class_='products wrapper grid products-grid').find('ol').find_all('li')

for item in all_items:
    name = item.find('strong').text.strip()
    img = item.find('img')['src']
    print(img)
    link = item.find('strong').find('a').get('href')
    driver.get(link)
    time.sleep(1)
    html_item_text = driver.page_source
    print(name)
    soup_item = BeautifulSoup(html_item_text, 'lxml')
    price = soup_item.find('div', class_='product-info-main').find('span', attrs={'data-price-amount':True}).text.strip()
    print(price)
    description = soup_item.find('div', class_='value').find('p').text.strip()
    print(description)
    all_features = ''
    features = soup_item.find('div', class_='value').find('div').find_all('h4')
    for feature in features:
        all_features += '-\t' + feature.text.strip() + '\n'
    print(all_features)
    data.append([name, price, description, all_features, img, link])
    
driver.quit()

with open(sub_directory_name, 'w', encoding='utf_8_sig') as w_csv_file:
    csv_writer = csv.writer(w_csv_file)
    csv_writer.writerow(['name', 'price', 'description', 'features', 'image link', 'link'])
    for line in data:
        csv_writer.writerow(line)
    



