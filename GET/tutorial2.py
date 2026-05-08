import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Dict

app = FastAPI()


def load_ecommerce_database():
    with open("ecommerce.json", "r") as file:
        return json.load(file)


class Orders(BaseModel):
    status: Optional[
        Annotated[
            str,
            Field(
                description="Status of the order",
                examples=["pending", "completed", "cancelled"],
            ),
        ]
    ] = None


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


@app.delete("/users/{user_id}/orders/{order_id}")
def delete_items(user_id: int, order_id: int):
    products_detail = load_ecommerce_database()

    del_products_info = []
    for details in products_detail:
        if details["id"] == user_id:
            for oder in details["orders"]:
                if oder["order_id"] == order_id:
                    del_products_info.append(oder)
                    details["orders"].remove(oder)
                    with open("ecommerce.json", "w") as file:
                        json.dump(products_detail, file, indent=4)

    return {
        "message": "Order {} deleted successfully".format(
            del_products_info[0]["order_id"]
        ),
        "deleted_order": {
            "order_id": del_products_info[0]["order_id"],
            "product": del_products_info[0]["product"],
            "status": del_products_info[0]["status"],
        },
    }


"""
        "order_id": 101,
        "product": "Laptop",
        "quantity": 1,
        "price": 1299.99,
        "status": "delivered",
        "ordered_at": "2024-11-01T10:30:00"
"""


class OrdersDetails(BaseModel):
    order_id: Annotated[
        int, Field(description="ID of the order", examples=[101, 102, 103])
    ]
    product: Annotated[
        str,
        Field(
            description="Name of the product", examples=["Laptop", "Mouse", "Keyboard"]
        ),
    ]
    quantity: Annotated[
        int, Field(description="Quantity of the product", examples=[1, 2, 3])
    ]
    price: Annotated[
        float,
        Field(description="Price of the product", examples=[1299.99, 49.99, 19.99]),
    ]
    status: Annotated[
        str,
        Field(
            description="Status of the order",
            examples=["pending", "completed", "cancelled"],
        ),
    ]
    ordered_at: Optional[
        Annotated[
            str,
            Field(
                description="Date and time when the order was placed",
                examples=["2024-11-01T10:30:00", "2024-11-02T14:45:00"],
            ),
        ]
    ] = None


@app.post("/users/{user_id}/orders")
def insert_recent_orders(user_id: int, order: OrdersDetails):
    ecommerce_database = load_ecommerce_database()

    for details in ecommerce_database:
        if details["id"] == user_id:
            details["orders"].append(order.model_dump())

    with open("ecommerce.json", "w") as file:
        json.dump(ecommerce_database, file, indent=2)

    return {"message": "Order added successfully", "order": order.model_dump()}


def load_users_database():
    with open("users.json", "r") as file:
        return json.load(file)


@app.get("/active-with-projects")
def find_details_active_users():
    user_database = load_users_database()

    active_users = []
    

    for details in user_database["users"]:
        if details["is_active"]:
            active_users.append(
                {
                    "id": details["id"],
                    "name": details["username"],
                    "email": details["email"],
                    "project_count": len(details["projects"]),
                }
            )

    return active_users