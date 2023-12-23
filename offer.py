
class Offer:
    def __init__(self ,title, price ,location , date, size, price_per_meter):
        self.negotiable = None
        self.title = comma_to_dot(title)
        # self.price = self.convert_price(comma_to_dot(price))
        self.price = comma_to_dot(price)
        self.location = remove_comma(location)
        self.date=  comma_to_dot(date)
        self.size = comma_to_dot(size)
        self.price_per_meter = self.convert_price_per_meter(comma_to_dot(price_per_meter))
    
    def print(self):
        print(self.title + " - "+ self.price + " - "+self.location+ " - "+self.date + " - "+self.size+" - "+self.price_per_meter+ " - negotiable: "+ str(self.negotiable) )
    def get(self):
        return [self.title, self.price,self.location,self.date,self.size,self.price_per_meter,self.negotiable]
    def convert_price(self,price:str):
        price = price.replace('zł','')
        if 'do negocjacji' in price:
            self.negotiable = True
            price = price.replace('do negocjacji','')
        else:
            self.negotiable = False
        return price
    def convert_price_per_meter(self,price_per_meter:str):
        return price_per_meter[:-5]

def comma_to_dot(string:str):
    return string.replace(',','.')
def remove_comma(string:str):
    return string.replace(',','')
   

