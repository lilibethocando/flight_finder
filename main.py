#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

# 4. Pass the data back to the main.py file, so that you can print the data from main.py

from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


ORIGIN_CITY_IATA = "ORD"

# print(sheet_data)

# 5. In main.py check if sheet_data contains any values for the "iataCode" key.
# If not, then the IATA Codes column is empty in the Google Sheet.
# In this case, pass each city name in sheet_data one-by-one to the FlightSearch class.
# For now, the FlightSearch class can respond with "TESTING" instead of a real IATA code.
# You should use the response from the FlightSearch class to update the sheet_data dictionary.

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_codes(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.now() + timedelta(days=1)
#five_month_from_today = datetime.now() + timedelta(days=5 * 30)
seven_month_from_today = datetime.now() + timedelta(days=7 * 30)

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=seven_month_from_today
    )
    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        ######################
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)
        #######################
        link = f"https://www.google.com/travel/flights?q=Flights%20to%20{flight.destination_airport}%20from%20{flight.origin_airport}%20on%20{flight.out_date}%20through%20{flight.return_date}"
        notification_manager.send_emails(emails, message, link)


        # notification_manager.send_sms(message)


