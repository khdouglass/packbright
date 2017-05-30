class SuggestedList(object):
    def __init__(self, location, weather_list, activities_list, num_days, outfit_sum):
        self.location = location
        self.weather_list = weather_list
        self.activities_list = activities_list
        self.num_days = num_days
        self.outfit_sum = outfit_sum
    
    def activities(self):
        items = []
        if 'Party' in self.activities_list:
            items.extend([('Vitamins / Medications', 'Advil'), ('Tolietries', 'Face Mask'),
                          ('Hair Products / Tools', ''), ('Make Up', '')])
        if 'Tourism' in self.activities_list:
            items.extend([('Shoes', 'Walking Shoes'), ('Technology', 'Camera'), ('Accessories', 'Travel Bag')])
        if 'Business / Work' in self.activities_list:
            items.extend([('Technology', 'Laptop'), ('Technology', 'Laptop Charger'), ('Suit', 'Suit'), 
                          ('Accessories', 'Work Bag/Briefcase')])
        if 'Working Out' in self.activities_list:
            items.extend([('Shoes', 'Work Out Shoes'),('Socks', 'Athletic Socks')])
        if 'Hiking' in self.activities_list:
            items.extend([('Shoes', 'Hiking Shoes'), ('Socks', 'Hiking Socks'), ('Skin Care', 'Bug Spray'),
                          ('Skin Care', 'Sunscreen'), ('Accessories', 'Backpack')])
        if 'Skiing' in self.activities_list:
            items.extend([('Jacket', 'Ski Jacket'), ('Pants', 'Ski Pants'), ('Socks', 'Ski Socks'),
                          ('Skin Care', 'Sunscreen'), ('Hat', 'Beanie'), ('Accessories', 'Gloves'), 
                          ('Outdoor Equipment', 'Skis')])
        if 'Camping' in self.activities_list:
            items.extend([('Outdoor Equipment', 'Tent'), ('Outdoor Equipment', 'Sleeping Bag'),
                          ('Outdoor Equipment', 'Cooking Supplies')])
        if 'Wedding / Special Event' in self.activities_list:
            items.extend([('Shoes', 'Formal Shoes'), ('Hair Products / Tools', ''), ('Make Up', '')])
        if 'Swimming' in self.activities_list:
            items.extend([('Swimsuit', 'Swimsuit'), ('Skin Care', 'Sunscreen'), ('Sandals', 'Sandals')])

        return items

    def need_passport(self):
        if unicode(' United States') in self.location:
            return False
        else:
            return True

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

    def misc_items(self):
        items = []
        if self.num_days:
            items.extend([('Sleepwear', 'Pajamas'), ('Technology', 'Cell Phone Charger')])
        items.extend([('Undergarments', self.outfit_sum)])

        return items