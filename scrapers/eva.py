import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

direcotory_name = os.path.dirname(__file__)
sub_directory_name = os.path.dirname(direcotory_name) + r'\excel\eva.csv'

array = []
data = []
with open('execl.csv', 'r') as r_csv_file:
    csv_reader = csv.reader(r_csv_file)

    for line in csv_reader:
        array.append(line)
    print(array)



  
#url of the page we want to scrape
baseURL = "https://shop.eva-cosmetics.com"
url = "https://shop.eva-cosmetics.com/en/products?categories=oral-care"
  
# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome() 
driver.get(url) 
  
# this is just to ensure that the page is loaded
time.sleep(10) 
  
html = driver.page_source
  
# this renders the JS code and stores all
# of the information in static HTML code.
  
# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "lxml")
items = soup.find_all(id="about", class_="ng-star-inserted")
counter = 1
for item in items:
    link = item.find('a', class_="main-text font-bold").get('href')
    driver.get(baseURL + link)
    time.sleep(10) 
    sub_html = driver.page_source
    #print(sub_html)
    sub_soup = BeautifulSoup(sub_html, "lxml")
    product_name = sub_soup.find('h1').text.strip()
    price = sub_soup.find('p', class_="primary-text").find(text=True, recursive=False).text.strip()
    description = sub_soup.find('div', class_="description").p.text.strip()
    data.append(["Eva", product_name, price, description])
    print(counter,'.')
    print("Product name: " + product_name)
    print("Price: " + price)
    print("Description: " + description)
    counter += 1
    
    



with open(sub_directory_name, 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    for line in array:
        csv_writer.writerow(line)
    for line in data:
        csv_writer.writerow(line)