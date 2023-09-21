import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Constants
DATABASE_NAME = 'brochures.db'
BIM_URL = 'https://www.bim.com.tr/Categories/680/afisler.aspx'
A101G_URL = 'https://www.a101.com.tr/aldin-aldin-gelecek-hafta-brosuru/'
A101B_URL = 'https://www.a101.com.tr/aldin-aldin-bu-hafta-brosuru/'
SOK_URL = 'https://kurumsal.sokmarket.com.tr/haftanin-firsatlari/firsatlar'
MIGROS_URL = 'https://www.money.com.tr/migroskop-dijital'

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dates (
            date_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            link_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_id INTEGER,
            link TEXT,
            FOREIGN KEY (date_id) REFERENCES dates (date_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_data_into_database(date, image_links):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert the date into the 'dates' table if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (date,))
    conn.commit()

    # Get the date_id for the current date
    cursor.execute("SELECT date_id FROM dates WHERE date=?", (date,))
    date_id = cursor.fetchone()[0]

    # Insert the links into the 'links' table with the associated date_id
    for image_link in image_links:
        cursor.execute("INSERT INTO links (date_id, link) VALUES (?, ?)", (date_id, image_link))
        conn.commit()

    conn.close()

def scrape_bim():
    r = requests.get(BIM_URL)
    source = BeautifulSoup(r.content, "lxml")
    items = source.find_all('div', class_='grup1 genelgrup col-12 col-md-6 rightArea')

    for item in items:
        date = item.find('span', class_='text').text.strip()
        image_links = ['https://www.bim.com.tr' + img['data-bigimg'] for img in item.find_all('a', class_='small')]
        
        insert_data_into_database(date, image_links)

def scrape_a101b():
    r = requests.get(A101B_URL)
    source = BeautifulSoup(r.content, "lxml")
    temp = source.find(class_="brochure-tabs")
    items = temp.find_all(class_="view-area")

    dates = temp.find(title="Aldın Aldın Bu Hafta")
    dates = str(dates.find(class_="dates"))
    date = dates.split('"')
    current_date = date[3].strip()  # Extract and clean the date
    
    insert_data_into_database(current_date, [item.find('img')['src'] for item in items])

def scrape_a101g():
    r = requests.get(A101G_URL)
    source = BeautifulSoup(r.content, "lxml")
    temp = source.find(class_="brochure-tabs")
    items = temp.find_all(class_="view-area")

    dates = temp.find(title="Aldın Aldın Gelecek Hafta")
    dates = str(dates.find(class_="dates"))
    date = dates.split('"')
    current_date = date[3].strip()  # Extract and clean the date
    
    insert_data_into_database(current_date, [item.find('img')['src'] for item in items])

def scrape_sok():
    r = requests.get(SOK_URL)
    source = BeautifulSoup(r.content, "lxml")
    temp = source.find_all('a')
    links = []

    for line in temp:
        link = line.get("href")
        links.append(link)

    current_date_sok = "Your Date Here"  # Replace with the actual date
    
    insert_data_into_database(current_date_sok, ['https://kurumsal.sokmarket.com.tr' + links[22], 'https://kurumsal.sokmarket.com.tr' + links[23]])

def scrape_migros():
    r = requests.get(MIGROS_URL)
    source = BeautifulSoup(r.content, "lxml")
    temp = source.find_all('button', class_="btn btn-white-purple-line center-block _df_button")
    link = [temp[0].get("source")]
    date= temp[0].get("mcdate")
    
    insert_data_into_database(date, link)

def reset_database():
    # Close any existing connections
    conn = sqlite3.connect(DATABASE_NAME)
    conn.close()
    
    # Delete the database file if it exists
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    
    # Recreate the database and tables
    initialize_database()

if __name__ == "__main__":
    reset_database()  # This will delete and recreate the database
    
    # Scraping and inserting data for BIM
    scrape_bim()
    
    # Scraping and inserting data for A101 Bu Hafta
    scrape_a101b()
    
    # Scraping and inserting data for A101 Gelecek Hafta
    scrape_a101g()
    
    # Scraping and inserting data for SOK
    scrape_sok()

    # Scraping and inserting data for MIGROS
    scrape_migros()
    
    # Run the Flask app
    app.run(debug=True)