import re
import requests
from bs4 import BeautifulSoup
import csv

data = []

baseURL = "https://cybeleegypt.com"

html_text = requests.get(baseURL + "/collections").text
soup = BeautifulSoup(html_text, "lxml")
collections = soup.find("div", class_="list-category row").find_all('div', class_="img_collection")

for collection in collections:
    link = collection.a.get("href")
    if "frontpage" in link:
        continue
    print(link)
    presub_html_text = requests.get(baseURL + link).text

    presub_soup = BeautifulSoup(presub_html_text, 'lxml')

    productsContainer = presub_soup.find("div", class_="product-grid-view grid-uniform").findAll('h4', class_="title-product")

    i = 1
    for container in productsContainer:
        link = container.a.get('href')
        sub_html_text= requests.get(baseURL + link).text
        sub_soup = BeautifulSoup(sub_html_text, "lxml")
        product_name = sub_soup.find('h2', class_="product-title").text.strip()
        price = re.findall(r'\d+', sub_soup.find(class_="enj-product-price engoj_price_main").text)[0]
        description = sub_soup.find('div', class_='pd_summary').p.text.strip()
        colorContainer = sub_soup.find('div', class_='maxus-productdetail__options')
        colorArr = []
        if colorContainer is not None:
            colorsContainer = colorContainer.find_all('div', attrs={'data-value' : True})
            for color in colorsContainer:
                colorValue = color.attrs['data-value']
                removable = re.findall(r"\|\d+",colorValue)
                if len(removable) > 0:
                    colorArr.append(color.attrs['data-value'].replace(removable[0], ''))
                else:
                    colorArr.append(color.attrs['data-value'])
        print(i, '\b.')
        print('\t' + product_name)
        print('\t' + price)
        print('\t' + description)
        print('\t' + "; ".join(colorArr))
        data.append([link ,product_name, price, description, "; ".join(colorArr)])
        with open('cybelle.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            for line in data:
                csv_writer.writerow(line)
        i += 1
