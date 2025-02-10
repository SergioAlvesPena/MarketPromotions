# Web Scrapping is a method to gather public data of web pages more info: https://oxylabs.io/blog/web-scraping

import requests
import pandas as pd
from bs4 import BeautifulSoup

def url_crawler():

    urls = []
    for page in range(1,6):
        print(f"Scraping page {page}.")
        response = requests.get(f"https://www.tiendeo.com.br/sorocaba/supermercados")
        html_doc = BeautifulSoup(response.text, "html.parser")

        for product in html_doc.find_all("div", class_="product-card"):
            link = product.select_one("a")
            urls.append("https://sandbox.oxylabs.io" + link.get("href"))
    return ""

def scraper(url):
    product_data = []
    #url = "https://www.tiendeo.com.br/sorocaba/supermercados"
    response = requests.get(url.strip())
    html_doc = BeautifulSoup(response.text, "html.parser")

    product_data.append({
        "title": html_doc.select_one("h2").get_text(),
        "price": html_doc.select_one(".price").get_text(),
        "developer": html_doc.select_one(".developer").get_text().replace("Developer: ", ""),
        "link": url.strip()
    })

def roldao_scraper():
    product_data = []
    url = "https://roldao.com.br/ofertas-do-roldao/"
    response = requests.get(url.strip())
    html_doc = BeautifulSoup(response.text, "html.parser")

    product_data.append({
        "title": html_doc.select_one(".entry-title").get_text(),
        "operation": html_doc.select_one(".post-excerpt").get_text(),
        "developer": html_doc.select_one(".developer").get_text().replace("Developer: ", ""),
        "link": url.strip()
    })
