import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import sqlite3

conn = sqlite3.connect('brochures.db')
cursor = conn.cursor()

url_bim = 'https://www.bim.com.tr/Categories/680/afisler.aspx'
url_a101g = 'https://www.a101.com.tr/aldin-aldin-gelecek-hafta-brosuru/'
url_a101b = 'https://www.a101.com.tr/aldin-aldin-bu-hafta-brosuru/'
url_sok = 'https://kurumsal.sokmarket.com.tr/haftanin-firsatlari/firsatlar'


#ŞOK

r_sok = requests.get(url_sok)
source_sok = BeautifulSoup(r_sok.content,"lxml")
temp_sok = source_sok.find_all('a')
links_sok = []
for line in temp_sok:
    link = line.get("href")
    links_sok.append(link)


print("ŞOK Aktüel Ürünler:")
print()
items_sok = ('https://kurumsal.sokmarket.com.tr'+links_sok[22], 'https://kurumsal.sokmarket.com.tr'+links_sok[23])
print(items_sok[0])
print(items_sok[1])
print()
# Get the current date for ŞOK
current_date_sok = "Your Date Here"  # Replace with the actual date

# Insert the date into the 'dates' table if it doesn't exist
cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (current_date_sok,))
conn.commit()

# Get the date_id for the current date
cursor.execute("SELECT date_id FROM dates WHERE date=?", (current_date_sok,))
date_id_sok = cursor.fetchone()[0]

# Insert the links into the 'links' table with the associated date_id
for item_sok in items_sok:
    # Insert the link into the 'links' table
    cursor.execute("INSERT INTO links (date_id, link) VALUES (?, ?)", (date_id_sok, item_sok))
    conn.commit()

# Close the connection
conn.close()
print()