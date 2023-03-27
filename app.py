from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import sqlite3, time, requests

url = "https://www.flipkart.com/search?q=iphone+14"


while True:
  response = requests.get(url)
  soupdata = soup(response.content, "html.parser")
  # print(soupdata)
  containers = soupdata.find_all('div', {'class': '_2kHMtA'})
  my_list = []
  
  for container in containers:
    name = container.find('div', {'class': '_4rR01T'})
    NAMES = name.text
    stars = container.find('div', {'class':'_3LWZlK'})
    try:
      STARS = stars.text
    except:
      STARS = 0

    ratings = container.find('span', {'class':'_2_R_DZ'})
    try:
      RATINGS = ratings.text
    except:
      RATINGS = 0
    prices = container.find('div', {'class': '_30jeq3 _1_WHN1'})
    PRICES = prices.text
    # print(NAMES, STARS, RATINGS, PRICES)
    # print('\n')
    my_tuple = (NAMES,STARS,RATINGS,PRICES)
    my_list.append(my_tuple)
  # print(my_list)
  nav = soupdata.find('nav', {'class': 'yFHi8N'})
  # print(nav)
  links = nav.find_all('a')
  print('links',links[-1].find('span'))

  url = 'https://www.flipkart.com'+links[-1]['href']

  if links[-1].find('span') is None:
    break
  
  print("url",url)
  time.sleep(1)
  conn = sqlite3.connect('test.db')
  conn.execute('''CREATE TABLE IF NOT EXISTS dicts
          (
          Product_name TEXT,
          Product_price TEXT,
          Product_rating TEXT,
          Product_stars TEXT);''')
  cur = conn.cursor()
  # cur.execute("DROP TABLE dicts")
  cur.executemany("""INSERT INTO dicts VALUES (?, ?, ?, ?)""", my_list)
  conn.commit()
  cur.close()