from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import csv
from offer import Offer
import random

NAMES_OF_CLASSES = {
    "title"                 :   "css-16v5mdi",
    "price"                 :   "css-10b0gli",
    "location_date"         :   "css-odp1qd",
    "size_price_per_meter"  :   "css-643j0o",
    "pages"                 :   "css-1mi714g"
}                           
file_name = "scraper\off.csv"

def location_n_date_splitter(text_to_split:str)-> str:
    parts = text_to_split.split("-")
    if len(parts) <= 1:
        return "",""
    elif len(parts) == 3:
        location = parts[0]
        date = parts[1]
    else:
        location = parts[0] + " " + parts[1]
        date = parts[2]

    parts = date.split(" ")
    if parts[1] == "Dzisiaj":
        date = parts[1] 
    else:
        date = parts[0] +" " +  parts[1] +" " + parts[2] +" "+  parts[3][:4]
    return location, date

def size_n_price_pm_splitter(text_to_split) ->str:
    parts = text_to_split.split("-")
    size = parts[0]
    price_pm = parts[1]
    return size, price_pm

def clear_csv():
    csv_file = open(file_name, 'w',newline = '',encoding="utf8")
    csv_file.close()

def save_offers_to_csv(file_name, offers):
    csv_file = open(file_name, 'a',newline = '',encoding="utf8")
    writer = csv.writer(csv_file,delimiter = ',')
    for offer in offers:
        writer.writerow(offer.get())
    csv_file.close()

def write_header(file_name):
    csv_file = open(file_name, 'a',newline = '',encoding="utf8")
    writer = csv.writer(csv_file,delimiter = ',')
    writer.writerow(['title','price','location','date','size','price_pm','negotiable'])
    csv_file.close()

def find_next_tag_by_class_name(tag, class_name):
    current_tag = tag
    safety_limit = 30
    while True:
        safety_limit-=1
        if current_tag.has_attr('class'):
            if current_tag.get("class")[0] == class_name:
                return current_tag
            else:
                current_tag = current_tag.find_next()
        else:
            current_tag = current_tag.find_next()
        if safety_limit<= 0:
            print("No tags")
            break
    
def find_number_of_pages(url):
    number_of_pages = 0
    page = urlopen(url)
    html = page.read()
    html = html.decode("utf-8")
    soup = BeautifulSoup(html,"html.parser")
    page_tags = soup.find_all("a", {"class": NAMES_OF_CLASSES["pages"]})
    number_of_pages = page_tags[-1].text
    return int(number_of_pages)

def find_good_pages(url,number_of_pages):
    good_pages = []
    for i in range(1,number_of_pages+1):
        cur_url = url + str(i)
        try:
            page = urlopen(cur_url)
        except:
            print("Page nr " + str(i) + " is fucked")
        else:
            good_pages.append(i)
    return good_pages
            

def scrap_single_page(url:str):
    page = urlopen(url)
    html = page.read()
    html = html.decode("utf-8")
    soup = BeautifulSoup(html,"html.parser")

    #   Save to txt for testing
    f = open("scraper/soup.txt",'w',encoding="utf8")
    f.write(str(soup))
    f.close()

    offer_tags = soup.find_all("div", {"class": "css-1apmciz"})
    offers = []

    for id_offer, offer_tag in enumerate(offer_tags):
        title_tag = find_next_tag_by_class_name(offer_tag,NAMES_OF_CLASSES["title"])
        title = title_tag.text
        price_tag = find_next_tag_by_class_name(title_tag,NAMES_OF_CLASSES["price"])
        price = price_tag.text
        location_n_date_tag = find_next_tag_by_class_name(price_tag,NAMES_OF_CLASSES["location_date"])
        location_n_date = location_n_date_tag.text
        location, date = location_n_date_splitter(location_n_date)
        size_n_price_pm_tag = find_next_tag_by_class_name(title_tag,NAMES_OF_CLASSES["size_price_per_meter"])
        size_n_price_pm = size_n_price_pm_tag.text
        size, price_pm = size_n_price_pm_splitter(size_n_price_pm)

        # print(title + " - " + price + " - " + location + " - " + date + " - "+ size + " - " + price_pm )

        offer_instance = Offer(title, price,location, date, size, price_pm)
        offers.append(offer_instance)
    save_offers_to_csv(file_name,offers)

def scrap_multiple_pages(number_of_pages:int,starting_url:str):
    good_pages = find_good_pages(starting_url,number_of_pages)
    random.shuffle(good_pages)
    
    for current_page_number,good_page in enumerate(good_pages):
        url =starting_url+ str(good_page)
        print(str(round(100.00*current_page_number/len(good_pages),2))+"%")
        scrap_single_page(url)

def main():
    url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?page="
    clear_csv()
    write_header(file_name)
    pages_to_scrap =  find_number_of_pages(url)
    scrap_multiple_pages(pages_to_scrap,url)

if __name__ == "__main__":
    main()



