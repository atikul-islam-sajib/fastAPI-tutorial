import json
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Dict

app = FastAPI()


def load_ecommerce_database():
    with open("ecommerce.json", "r") as file:
        return json.load(file)

class Orders(BaseModel):
    status: Optional[Annotated[str, Field(description="Status of the order", examples=["pending", "completed", "cancelled"])]] = None

@app.get("/user/{user_id}/{orders}")
def display_all_delivered_orders(user_id: int, status: str):

    products_detail = load_ecommerce_database()

    specific_details = []

    for details in products_detail:
        while user_id == details["id"]:
            specific_details.append(details)
            break

    ordered_information = []

    for details in specific_details:
        delivered_information = details["orders"]
        for order in delivered_information:
            if order["status"] == status:
                ordered_information.append(order)

    result = {
        "user_id": specific_details[0]["id"],
        "name": specific_details[0]["name"],
        "orders": ordered_information,
        "total_results": len(ordered_information),
    }
    return result


@app.get("/users")
def filter_dataset(role: str, active: bool, city: str):
    users_information = load_ecommerce_database()

    detailed_information = []

    for details in users_information:
        while (
            details["role"] == role
            and details["active"] == active
            and details["address"]["city"] == city
        ):
            detailed_information.append(
                {
                    key: value
                    for key, value in details.items()
                    if key not in ["orders", "created_at", "tags"]
                }
            )
            break

    return {
        "total": len(detailed_information),
        "users": detailed_information,
    }

@app.put("/users/{user_id}/orders/{order_id}")
def update_details(user_id: int, order_id: int, status: Orders):
    orders_detail = load_ecommerce_database()
    
    specific_information = []
    orders_information = []
    for details in orders_detail:
        if details["id"] == user_id:
            specific_information.append(details)

    for details in specific_information:
        for order in details["orders"]:
            if order["order_id"] == order_id:
                order["status"] = status.status
                orders_information.append(order)
                with open("ecommerce.json", "w") as file:
                    json.dump(orders_detail, file, indent=4)
        
                
    return orders_information