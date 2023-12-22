from urllib.request import urlopen
from bs4 import BeautifulSoup
from offer import Offer


url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/"
text_file = "text.txt"

page = urlopen(url)

html = page.read()
html = html.decode("utf-8")

soup = BeautifulSoup(html,"html.parser")

file = open(text_file, 'w',encoding="utf8")
file.write(str(soup))
file.close()

offer_titles = soup.find_all("h6", {"class": "css-16v5mdi er34gjf0"})

number_of_offers = len(offer_titles)
offers = []

for id_offer, offer_title_tag in enumerate(offer_titles):
    offer_price = offer_title_tag.find_next().text
    # print(offer_price)
    offer_location = offer_title_tag.parent.find_next().find_next().text
    print(offer_location)
    #offer_instance = Offer(offer_title.text,offer_price)
    #offers.append(offer_instance)


