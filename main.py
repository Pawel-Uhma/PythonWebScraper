from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from offer import Offer

NAMES_OF_CLASSES = {
    "title"                 :   "css-16v5mdi",
    "price"                 :   "css-10b0gli",
    "location_date"         :   "css-veheph",
    "size_price_per_meter"  :   "css-643j0o"
}                           
url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/"
file_name = "off.csv"

def location_n_date_splitter(text_to_split:str)-> str:
    parts = text_to_split.split("-")
    if len(parts) <= 1:
        return "",""
    elif len(parts) == 3:
        location = parts[0] +" "+ parts[1]
        date = parts[2]
    else:
        location = parts[0]
        date = parts[1]
    return location, date

def size_n_price_pm_splitter(text_to_split) ->str:
    parts = text_to_split.split("-")
    size = parts[0]
    price_pm = parts[1]
    return size, price_pm

    
def save_offers_to_csv(file_name, offers):
    csv_file = open(file_name, 'w',newline = '',encoding="utf8")
    writer = csv.writer(csv_file,delimiter = ',')
    for offer in offers:
        writer.writerow(offer.get())
    csv_file.close()

def scrap_offers():
    page = urlopen(url)
    html = page.read()
    html = html.decode("utf-8")
    soup = BeautifulSoup(html,"html.parser")

    f = open("text.txt",'w',encoding="utf8")
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
        # print(price + " - " + location + " - " + date + " - "+ size + " - " + price_pm )
        offer_instance = Offer(title, price,location, date, size, price_pm)
        offers.append(offer_instance)
    save_offers_to_csv(file_name,offers)

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
            break
    

if __name__ == "__main__":
    scrap_offers()



