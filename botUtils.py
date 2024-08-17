

class Film:
    def __init__(self,title,description,year,special_features,full_name,category_name):
        self.title = title
        self.description = description
        self.year = year
        self.features = special_features
        self.full_name = full_name
        self.category_name = category_name
    def __str__(self):
        return (f'Title: {self.title}\n'
                f'Description: {self.description}\n'
                f'Year: {self.year}\n'
                f'Special Features: {self.features}\n'
                f'Full Name: {self.full_name}\n'
                f'Category: {self.category_name}')

def get_columns(res):
    if res:
        messages=[]
        for film_data in res:
            title, description, year, special_features, full_name, category_name = film_data
            film = Film(title, description, year, special_features, full_name, category_name)
            messages.append(str(film))
        return messages
    else:
        return "No results found for your keyword."