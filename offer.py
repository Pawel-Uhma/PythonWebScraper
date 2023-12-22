
class Offer:
    def __init__(self ,title ,price ,size ,location) -> None:
        self.title = title
        self.price = price
        self.size = size
        self.location = location
        self.negotiable = None
        return self
    def print(self):
        print(self.title + " - "+ self.price + " - "+self.size + " - "+self.location )

        