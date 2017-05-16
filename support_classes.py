class SuggestedList(object):
    def __init__(self, num_outfits, location, weather_list):
        self.location = location
        self.weather_list = weather_list
        self.num_outfits = int(num_outfits)
        self.num_socks = int(num_outfits) / 2 

    def need_passport(self):
        if 'United States' in self.location:
            return False

    def need_sunglasses(self):
        for item in self.weather_list:
            if 'Clear' in item:
                return True

    def need_jacket(self):
        for item in self.weather_list:
            if int(item[3]) < 55:
                return True

    def need_umbrella(self):
        for item in self.weather_list:
            if item[1] in ['Rain', 'Thunderstorms', 'Sleet', 'Chance of Rain']:
                return True
