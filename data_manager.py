from pprint import pprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bearer_headers = {
    "Authorization": TOKEN
}

SHEETY_PRICES_ENDPOINT = os.getenv('SHEETY_PRICES_ENDPOINT')
SHEET_USERS_ENDPOINT = os.getenv('SHEET_USERS_ENDPOINT')

class DataManager:
    def __init__(self):
        self.destination_data = {}


    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=bearer_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        # 3. Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id  from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    # HINT: Remember to check the checkbox to allow PUT requests in Sheety.

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "city": city["city"],
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                #headers= bearer_headers,
                json=new_data
            )
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = SHEET_USERS_ENDPOINT
        response = requests.get(customers_endpoint, headers=bearer_headers)
        data = response.json()
        print(data)
        self.customer_data = data["users"]
        return self.customer_data

