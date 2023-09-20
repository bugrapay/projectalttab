import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)
api = Api(app)

conn = sqlite3.connect('brochures.db')
cursor = conn.cursor()

url_bim = 'https://www.bim.com.tr/Categories/680/afisler.aspx'
url_a101g = 'https://www.a101.com.tr/aldin-aldin-gelecek-hafta-brosuru/'
url_a101b = 'https://www.a101.com.tr/aldin-aldin-bu-hafta-brosuru/'
url_sok = 'https://kurumsal.sokmarket.com.tr/haftanin-firsatlari/firsatlar'


#BİM

r_bim = requests.get(url_bim)
source_bim = BeautifulSoup(r_bim.content,"lxml")
items_bim = source_bim.find_all('div', class_='grup1 genelgrup col-12 col-md-6 rightArea')

print("BİM Aktüel Ürünler:")
print()
for item in items_bim:
    date = item.find('span', class_='text').text.strip()
    image_links = [img['data-bigimg'] for img in item.find_all('a', class_='small')]
    first_img = source_bim.find('a', class_='fancyboxImage', rel='gallery1')
    image_url = first_img['href']
    print(date)
    print('https://www.bim.com.tr'+image_url)
    for image_link in image_links:
        print('https://www.bim.com.tr'+str(image_link))
    print()

    cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (date,))
    conn.commit()

    # Get the date_id for the current date
    cursor.execute("SELECT date_id FROM dates WHERE date=?", (date,))
    date_id = cursor.fetchone()[0]

    # Insert the links into the 'links' table with the associated date_id
    for image_link in image_links:
        cursor.execute("INSERT INTO links (date_id, link) VALUES (?, ?)", (date_id, 'https://www.bim.com.tr' + image_link))
        conn.commit()

conn.close()
print()
print()



#A101 Bu Hafta

r_a101b = requests.get(url_a101b)
source_a101b = BeautifulSoup(r_a101b.content,"lxml")
temp_a101b = source_a101b.find(class_="brochure-tabs")
items_a101b = temp_a101b.find_all(class_="view-area")

print("A101 Aktüel Ürünler:")
print()
dates = temp_a101b.find(title="Aldın Aldın Bu Hafta")
dates = str(dates.find(class_="dates"))
date = dates.split('"')
current_date = date[3].strip()  # Extract and clean the date
# Insert the date into the 'dates' table if it doesn't exist
cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (current_date,))
conn.commit()

# Get the date_id for the current date
cursor.execute("SELECT date_id FROM dates WHERE date=?", (current_date,))
date_id = cursor.fetchone()[0]

# Insert the links into the 'links' table with the associated date_id
print()
for item in items_a101b:
    first_img = item.find('img')
    image_url = first_img['src']
    # Insert the link into the 'links' table
    cursor.execute("INSERT INTO links (date_id, link) VALUES (?, ?)", (date_id, image_url))
    conn.commit()
    print(image_url)
# Close the connection
conn.close()
print()
print()


#A101 Gelecek Hafta

r_a101g = requests.get(url_a101g)
source_a101g = BeautifulSoup(r_a101g.content,"lxml")
temp_a101g = source_a101g.find(class_="brochure-tabs")
items_a101g = temp_a101g.find_all(class_="view-area")

print("A101 Aktüel Ürünler:")
print()
dates = temp_a101g.find(title="Aldın Aldın Gelecek Hafta")
dates = str(dates.find(class_="dates"))
date = dates.split('"')
current_date = date[3].strip()  # Extract and clean the date
# Insert the date into the 'dates' table if it doesn't exist
cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (current_date,))
conn.commit()

# Get the date_id for the current date
cursor.execute("SELECT date_id FROM dates WHERE date=?", (current_date,))
date_id = cursor.fetchone()[0]
print()
for item in items_a101g:
    first_img = item.find('img')
    image_url = first_img['src']
    print(image_url)
    # Insert the link into the 'links' table
    cursor.execute("INSERT INTO links (date_id, link) VALUES (?, ?)", (date_id, image_url))
    conn.commit()
    print(image_url)
# Close the connection
conn.close()
print()
print()


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


@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dates.date, GROUP_CONCAT(links.link, ', ') 
        FROM dates 
        LEFT JOIN links ON dates.date_id = links.date_id 
        GROUP BY dates.date
    """)
    data = cursor.fetchall()
    conn.close()

    # Convert data to a list of dictionaries
    result = [{"date": row[0], "links": row[1].split(', ')} for row in data if row[0] is not None]

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=False)