from flight_recommendations.flight import flight
from place_recommender.random_city import get_random_cities

from weather_module.weather import weather


def main(count):
    print("Hello! Where would you like to travel?")
    # cities = get_random_cities(exclude_city)
    # print(cities)
    # city = [word.strip().lower() for word in cities.split(",") if word.strip()]
    # city = [country.lower() for country in cities]
    # print(city)
    i = 0
    count += 1
    # print(count)
    # print(f"Here are 3 cities you might like: {cities}")
    # user_city = input("Do you like any city from the list, if yes: \nType a city from the list orelse type 'no': ").strip().lower()
    # if user_city in city:
    print("Okay! Fetching weather information for your selected city...")
    # weather(user_city, "2025-03-18", "2025-03-19")
    weather("Mumbai", "2025-03-18", "2025-03-19")
    start_date = "2025-03-18"
    end_date = "2025-03-19"
    user_city = "Mumbai"
    flight("YYZ", user_city, start_date, end_date, "")
    # next_flight = input("Do you like this flight option, if yes: enter yes or enter no: ").lower()
    # if next_flight == "no":
    #     flight(user_city, 1, start_date, end_date, "")
    #     next_flight1 = input("Do you like this flight option, if yes: enter yes or enter no: ").lower()
    #     if next_flight1 == "no":
    #         flight(user_city, 2, start_date, end_date, "")
    #         next_flight2 = input("Do you like this flight option, if yes: enter yes or enter no: ").lower()
    #         if next_flight2 == "no":
    #             print("No other option available.") 
    #         else:
                
    #             print("Added to calendar")
    #     else:
    #         print("Added to calendar")
    # else:
    print("Added to calendar")

    # else:
    #     print("Invalid choice. Try again after sometime.")

if __name__ == "__main__":
    count = 0
    i = 0
    exclude_city = []
    main(count)
