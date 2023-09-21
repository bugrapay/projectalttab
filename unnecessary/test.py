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


r = requests.get(MIGROS_URL)
source = BeautifulSoup(r.content, "lxml")
temp = source.find_all('button', class_="btn btn-white-purple-line center-block _df_button")
print(temp)
link = temp[0].get("source")
print(link)
date= temp[0].get("mcdate")
print(date)
