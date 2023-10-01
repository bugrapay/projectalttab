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
MIGROS_URL = 'https://www.money.com.tr/migroskop-dijital'
GRATIS_URL = 'https://view.publitas.com/gratis'


r = requests.get(GRATIS_URL)
source = BeautifulSoup(r.content, "lxml")
# Find the relevant img element
img_element = source.find_all('div')
print(img_element)
# Extract the image source (link)
#image_link = img_element.get['src']

# Print the extracted image link
#print(image_link)