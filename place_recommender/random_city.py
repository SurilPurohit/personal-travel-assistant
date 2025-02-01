import random


def get_random_cities(exclude_city):
    cities = [
        "Paris", "Tokyo", "Rio de Janeiro", "Sydney", "Toronto", "Delhi",
        "Rome", "Seoul", "Munich", "Barcelona",
        "New York", "London", "Beijing", "Mexico City", "Amsterdam",
        "Zurich", "Stockholm", "Moscow", "Buenos Aires", "Cape Town", "Mumbai"
    ]
    updated_cities = [item for item in cities if item not in exclude_city]
    return random.sample(updated_cities, 3)