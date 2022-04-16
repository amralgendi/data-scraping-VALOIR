from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

data = []

baseURL = "https://www.anastasiabeverlyhills.com"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Firefox() 
driver.get(baseURL) 
  
# this is just to ensure that the page is loaded
time.sleep(3) 
  
html = driver.page_source
soup = BeautifulSoup(html, "lxml")
nav = soup.find('div', class_='nav-links-wrap')
sections = nav.findAll('section')
for section in sections:
    if section.attrs['class'][1] == 'global' or section.attrs['class'][1] == 'main' or section.attrs['class'][1] == 'brushes' or section.attrs['class'][1] ==  'promotional':
        continue
    category = section.attrs['class'][1]
    subcategory_section = section.ul.find_all('li')
    for subcategory in subcategory_section:
        if bool(subcategory.attrs):
            continue
        print(subcategory.a.text)
        print(subcategory.a.get('href'))
        driver.get(subcategory.a.get('href')) 
  
        # this is just to ensure that the page is loaded
        time.sleep(3) 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        sub_html = driver.page_source
        sub_soup = BeautifulSoup(sub_html, "lxml")
        subcategory_container = sub_soup.find('div', id="search-result-items")
        product_container = subcategory_container.find_all('div', class_="col grid-tile", attrs={'data-list' : True})
        for product in product_container:
            product_name = product.find('div', class_="product-name").a.text.strip()
            print(product_name)
            link = product.find('div', class_="product-name").a.get('href')
            if 'http' in link:
                driver.get(link)
            else:
                driver.get(baseURL + link)
            time.sleep(3) 
            sub_sub_html = driver.page_source
            sub_sub_soup = BeautifulSoup(sub_sub_html, "lxml")
            price = sub_sub_soup.find('div', class_='product-price').find('span').text.strip()
            description = sub_sub_soup.find('div', class_='long-description').find('p').text.strip()
            what_i_love = ''
            ingredients = ''
            what_i_love_container = sub_sub_soup.find('div', class_='loveit dropdown-container')
            if what_i_love_container is not None: 
                what_i_love = what_i_love_container.text.strip()
            ingredients_container = sub_sub_soup.find('div', class_="product-ingredients-tab")
            if ingredients is not None:
                ingredients = ingredients_container.find(text=True, recursive=False)
            description = description.replace('\u2010', '-')
            ingredients = ingredients.replace('\u2010', '-')
            what_i_love = what_i_love.replace('\u2010', '-')
            color_arr = []
            color_container = sub_sub_soup.find('ul', class_="swatches color")
            if color_container is not None: 
                color_container_arr =  color_container.find_all('li', attrs={'aria-label' : True})
                for color in color_container_arr:
                    color_arr.append(color.attrs['aria-label'])
            data.append([category, subcategory.a.text, product_name, price, '; '.join(color_arr), description, what_i_love, ingredients])
            print(product_name)
            print(price)



with open('anastasia.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    for line in data:
        csv_writer.writerow(line)