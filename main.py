from flight_recommendations.flight import flight
from place_recommender.random_city import get_random_cities

from weather_module.weather import weather


def main(count, i):
    print("Hello! Where would you like to travel?")
    cities = get_random_cities(exclude_city)
    # print(cities)
    # city = [word.strip().lower() for word in cities.split(",") if word.strip()]
    city = [country.lower() for country in cities]
    # print(city)
    print(f"Here are 3 cities you might like: {cities}")
    user_city = input("Do you like any city from the list, if yes: \nType a city from the list orelse type 'no': ").strip().lower()
    if user_city in city:
        print("Okay! Fetching weather information for your selected city...")
        weather(user_city)
        flight(user_city, i)
    elif user_city == "no":
        if count < 2:
            print("We'll give you different cities to select. Thankyou for your patience.")
            main(count)
            exclude_city.append(cities)
    elif count < 2:
            print("We'll give you different cities to select. Thankyou for your patience.")
            main(count)
    else:
        print("Invalid choice. Try again after sometime.")

    count += 1
    i += 1    

if __name__ == "__main__":
    count = 0
    i = 0
    exclude_city = []
    main(count, i)
