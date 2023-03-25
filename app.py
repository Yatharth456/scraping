import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS scrape
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Product_name TEXT,
         Product_price TEXT,
         Product_rating TEXT,
         Product_desc TEXT);''')
cur = conn.cursor()

print("TABLE CREATED")

Product_name = []
Product_price = []
Product_desc = []
Product_rating = []


# for i in range(1,12):
url = "https://www.flipkart.com/search?q=xiaomi%20mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")
# print(soup.prettify())
limited_data = soup.find("div", class_ = "_1YokD2 _3Mn1Gg")

names = limited_data.find_all("div", class_ = "_4rR01T")

for i in names:
    name = i.text
    Product_name.append(name)

prices = limited_data.find_all("div", class_ ="_30jeq3 _1_WHN1")
for i in prices:
    price = i.text
    Product_price.append(price)

description = limited_data.find_all("ul", class_ = "_1xgFaf")
for i in description:
    review = i.text
    Product_desc.append(review)

ratings = limited_data.find_all("div", class_ = "_3LWZlK")
for i in ratings:
    rating = i.text
    Product_rating.append(rating)

my_dict = [{
    "Product_name": Product_name,
    "Product_price": Product_price,
    "Product_rating": Product_rating,
    "Product_desc.": Product_desc
}]

columns = list(my_dict[0].keys())
print(columns,"colums")
# sql_cmd = 'INSERT INTO scrape ({}) VALUES ({})'.format('.'.join(columns), ','.join(['?'] * len(columns)))

for data in my_dict:
    values = [data[column] for column in columns]
    conn.execute('INSERT INTO scrape ({}) VALUES ({})'.format('.'.join(columns), ','.join(['?'] * len(columns))), values)

conn.commit()
print ("Records created successfully")
cur.close()















# cur.execute("""INSERT INTO scrap (Product_name, Product_price, Product_rating, Product_desc) VALUES (?, ?, ?, ?)""",
    #             (str(my_dict['Product Name']), str(my_dict['Product Price']), str(my_dict['Product Rating']), str(my_dict['Product Desc.'])))