import json
class Auction:
    def __init__(self, id, description, starting_bid, duration, image_url=None):
        self.id = id
        self.description = description
        self.starting_bid = starting_bid
        self.duration = duration
        self.image_url = image_url

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def __str__(self):
        return self.to_json()