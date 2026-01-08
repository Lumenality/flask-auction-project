import json
class Auction:
    def __init__(self, id, description, starting_bid, auction_duration, image_url=None):
        self.id = id
        self.description = description
        self.starting_bid = starting_bid
        self.auction_duration = auction_duration
        self.image_url = image_url

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def __str__(self):
        return self.to_json()