from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from offer import Offer

name_of_classes = {
    "title"                 :   "css-16v5mdi er34gjf0",
    "price"                 :   "css-10b0gli er34gjf0",
    "location_date"         :   "css-veheph er34gjf0",
    "size_price_per_meter"  :   "css-643j0o"
}                           


def location_size_splitter(text_to_split:str)-> str:
    part = text_to_split.split("-")
    if len(part) <= 2:
        return "","","",""
    location = part[0]
    price_per_meter = part[2]
    date_n_size = part[1]
    date, size = split_date_from_size(date_n_size)
    return location, date, size, price_per_meter

def split_date_from_size(text_to_split) ->str:
    splitted = text_to_split.split()
    if splitted[0] == "Dzisiaj":
        date = splitted[0]+" "+ splitted[2][:5]
        size= splitted[2][5:]
        return date, size
    
    if len(splitted) >= 3:
        date = splitted[0] + " " + splitted[1] + " " +splitted[2][:4]
        size = splitted[2][4:]
        return date,size
    else: 
        return "",""
    
def save_offers_to_csv(file_name, offers):
    csv_file = open(file_name, 'w',newline = '',encoding="utf8")
    writer = csv.writer(csv_file,delimiter = ',')
    for offer in offers:
        # offer.print()
        writer.writerow(offer.get())
    csv_file.close()

def scrap_offers():
    url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/"
    file_name = "off.csv"
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
        title_tag = offer_tag.find_next().find_next()
        title = title_tag.text
        price_tag = title_tag.find_next()
        price = price_tag.text
        location_tag = price_tag.find_next().find_next()
        location_n_size = location_tag.text
        location, date, size, price_per_meter = location_size_splitter(location_n_size)
        print(price + " - " + size + " - " + price_per_meter + " - " + date)
        offer_instance = Offer(title, price,location, date, size, price_per_meter)
        offers.append(offer_instance)
    save_offers_to_csv(file_name,offers)

def find_next_tag_by_class_name(tag, class_name):
    current_tag = tag
    while True:
        if not current_tag.has_attr('class'):
            current_tag = current_tag.find_next()
        else:
            if current_tag['class'][0] == class_name:
                return current_tag
            else:
                current_tag = current_tag.find_next()
    

if __name__ == "__main__":
    scrap_offers()



