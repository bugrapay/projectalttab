import requests
from bs4 import BeautifulSoup

url_bim = 'https://www.bim.com.tr'
url_a101 = 'https://www.a101.com.tr'
url_sok = 'https://www.sokmarket.com.tr'


r_bim = requests.get(url_bim)
source_bim = BeautifulSoup(r_bim.content,"lxml")
#print(source)

inner_triangle_div = source_bim.find('div', class_='inner triangle')

a_tags = inner_triangle_div.find_all('a', class_='subButton')

links=[]

for a_tag in a_tags:
    span_text = a_tag.find('span', class_='text').text
    print(url_bim+a_tag.get("href"), span_text)
    a = (url_bim+a_tag.get("href"))
    links.append(a)


for link in links:
    products = requests.get(link)
    products_bim = BeautifulSoup(products.content,"lxml")
    product_list = products_bim.find('div', class_='productArea')
    productss = product_list.find_all('div', class_='inner')
    print('___________________________________________')
    for product in productss:
        if product.find('h2', class_='subTitle')==None :
            continue
        else:
            img = str(product.find('img', class_='img-fluid', xsrc_=''))
            img_link = img.split('"')
            prod = (product.find('h2', class_='subTitle').text+' '+product.find('h2', class_='title').text, product.find('div', class_='text quantify').text+''+product.find('span', class_='number').text, url_bim+img_link[3])
            print(prod)

