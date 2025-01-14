import json
import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionQueryProducts(Action):
    def name(self) -> Text:
        return "action_query_products"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Fetch preferences
        budget = tracker.get_slot("budget")
        brand = tracker.get_slot("brand")

        try:
            # Load the JSON database
            with open("db.json", "r") as db_file:
                data = json.load(db_file)
            
            # Query the JSON data
            query = {
                "price": int(budget),
                "brand": brand
            }
            products = [
                product for product in data["products"]
                if product["price"] <= query["price"] and product["brand"].lower() == query["brand"].lower()
            ]

            # Prepare and send the response
            if products:
                dispatcher.utter_message(text="Here are some products I found:")
                for product in products:
                    dispatcher.utter_message(text=f"{product['product_name']} - ₹{product['price']}")
            else:
                dispatcher.utter_message(text="No products found matching your criteria.")

        except Exception as e:
            logging.error(f"Error querying JSON database: {e}")
            dispatcher.utter_message(text="There was an error while fetching the products. Please try again later.")

        return []
