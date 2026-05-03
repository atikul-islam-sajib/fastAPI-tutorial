import json
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, Annotated, List, Dict

app = FastAPI()


def load_dataset():
    with open("database.json", "r") as file:
        return json.load(file)


def save_dataset(data):
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)


class Students(BaseModel):
    id: Annotated[
        int, Field(..., description="The ID of the student", examples=[1, 2, 3])
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="The name of the student",
            examples=["Lena Fischer", "John Doe", "Emma Smith"],
        ),
    ]
    age: Annotated[
        int, Field(..., description="The age of the student", examples=[20, 21, 22])
    ]
    email: Annotated[
        str,
        Field(
            ...,
            description="The email of the student",
            examples=[
                "lena.fischer@example.com",
                "john.doe@example.com",
                "emma.smith@example.com",
            ],
        ),
    ]
    is_active: Annotated[
        bool,
        Field(
            ...,
            description="Whether the student is active or not",
            examples=[True, False],
        ),
    ]
    enrolled_courses: Annotated[
        List[int],
        Field(
            ...,
            description="The list of courses the student is enrolled in",
            examples=[[101, 102], [201, 202], [301, 302]],
        ),
    ]
    profile: Annotated[
        Dict[
            str,
            Annotated[
                Optional[str], Field(..., description="The profile of the student")
            ],
        ],
        Field(
            ...,
            description="The profile of the student",
            examples=[
                {"major": "Computer Science", "year": 2, "gpa": 3.7},
                {"major": "Mathematics", "year": 3, "gpa": 3.9},
                {"major": "Physics", "year": 1, "gpa": 3.5},
            ],
        ),
    ]


class Courses(BaseModel):
    id: Annotated[
        int, Field(..., description="The ID of the course", examples=[101, 102, 103])
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="The name of the course",
            examples=["Introduction to Programming", "Data Structures", "Algorithms"],
        ),
    ]
    credits: Annotated[
        int,
        Field(
            ...,
            description="The number of credits for the course",
            examples=[5, 4, 3],
        ),
    ]
    instructor: Annotated[
        str,
        Field(
            ...,
            description="The name of the instructor",
            examples=["Dr. Klein", "Dr. Smith", "Dr. Johnson"],
        ),
    ]


class Grades(BaseModel):
    student_id: Annotated[
        int, Field(..., description="The ID of the student", examples=[1, 2, 3])
    ]
    course_id: Annotated[
        int, Field(..., description="The ID of the course", examples=[101, 102, 103])
    ]
    grade: Annotated[
        str,
        Field(
            ...,
            description="The grade of the student in the course",
            examples=["A", "B", "C"],
        ),
    ]


# Query: Get all students
# To execute the program
# 1. localhost:8000/students
# 2. localhost:8000/docs
@app.get("/students")
def display_all_students():
    dataset = load_dataset()
    return dataset


# Query: Get a specific student by ID
@app.get("/student/{student_id}")
def display_specific_student_detail(
    student_id: int = Path(..., description="The ID of the student")
):
    student_details = load_dataset()["students"]

    return student_details[student_id - 1]


# Query: Which courses is a student enrolled in ?
@app.get("/courses/{student_id}")
def show_course_details(
    student_id: int = Path(..., description="The ID of the student")
):
    data = load_dataset()
    students = data["students"]
    courses = data["courses"]

    enrolled_course_ids = []

    for student in students:
        if student_id == student["id"]:
            enrolled_course_ids.extend(student["enrolled_courses"])

    course_information = []

    for course_id in enrolled_course_ids:
        for course in courses:
            if course_id == course["id"]:
                course_information.append(
                    {"course_name": course["name"], "instructor": course["instructor"]}
                )

    return course_information


# Query: Find which grade a student got in a specific course
@app.get("/grades/{student_id}")
def display_student_grade(
    student_id: int = Path(..., description="The ID of the student")
):
    grade_details = load_dataset()["grades"]
    course_details = load_dataset()["courses"]

    grades = list()

    for grade in grade_details:
        if student_id == grade["student_id"]:
            grades.append(
                {
                    "course name".title(): [
                        course["name"]
                        for course in course_details
                        if grade["course_id"] == course["id"]
                    ][0],
                    "grade".title(): grade["grade"],
                }
            )
    return grades


# Query: How many courses all students enrolled in ?
@app.get("/enrolled_courses")
def enrolled_courses():
    student_details = load_dataset()["students"]

    information = list()

    for student in student_details:
        information.append(
            {student["name"]: "Enrolled in " + str(len(student["enrolled_courses"]))}
        )

    return information


# Query: Which student would get scholarship ?
@app.get("/scholarship")
def show_scholarship_students():
    student_details = load_dataset()["students"]

    information = list()

    for student in student_details:
        if student["is_active"] == True and student["profile"]["gpa"] > 3.5:
            information.append({student["name"]: "You are eligible for scholarship"})

    return information


# Query: I want to add one filed that is scholarship in the students details
@app.get("/scholarship/details")
def display_scholarship_details():
    students_information = load_dataset()["students"]

    for student in students_information:
        if student["is_active"] == True and student["profile"]["gpa"] > 3.5:
            student["scholarship"] = "You are eligible for scholarship"
            save_dataset(students_information)

    return students_information


# Grade A: find that student name, course name, course credit
@app.get("/grade/{grade}")
def show_details_about_students(
    grade: str = Path(..., description="The grade of the student")
):
    student_details = load_dataset()[
        "students"
    ]  # It will return a list of dictornaries
    course_details = load_dataset()["courses"]  # It will return a list of dictornaries
    grade_details = load_dataset()["grades"]  # It will return a list of dictornaries

    information = []

    for details in grade_details:
        if details["grade"] == grade:
            information.append(
                {"course_id": details["course_id"], "student_id": details["student_id"]}
            )

    courses = []
    # information: list of dictornary : [{"course_id": 103, "student_id": 2}]
    for details in course_details:
        for info in information:
            if details["id"] == info["course_id"]:
                courses.append(
                    {"name": details["name"], "instructor": details["instructor"]}
                )

    students = []
    for details in student_details:
        for info in information:
            if details["id"] == info["student_id"]:
                students.append({"name": details["name"]})

    return {"students": students, "courses": courses}


# Products Query


def load_dataset_ecommerce():
    with open("products.json", "r") as file:
        return json.load(file)


"""
  "orders": [
    {
      "id": 5001,
      "user_id": 1,
      "items": [
        {
          "product_id": 101,
          "quantity": 1
        },
        {
          "product_id": 102,
          "quantity": 2
        }
      ],
      "total_price": 1500.50,
      "status": "completed"
    }
  ]
}

 "products": [
    {
      "id": 101,
      "name": "Laptop",
      "price": 1200.50,
      "stock": 10
    },
    {
      "id": 102,
      "name": "Headphones",
      "price": 150.00,
      "stock": 25
    }
  ],
"""


@app.get("/user/{user_id}")
def display_all_completed_products(
    user_id: int = Path(..., description="The ID of the user")
):
    orders_detail = load_dataset_ecommerce()  # It will return a list of dictornaries
    products_detail = load_dataset_ecommerce()

    orders_information = []

    for order in orders_detail["orders"]:
        if "completed" == order["status"] and user_id == order["user_id"]:
            orders_information.append(order)

    informations = []
    products_info = []
    for order in orders_information:
        product_id = order["items"]
        for product in products_detail["products"]:
            for each_product in product_id:
                if product["id"] == each_product["product_id"]:
                    products_info.append({"name": product["name"], "quantity": each_product["quantity"]})

        informations.append(
            {
                "order_id": order["id"],
                "products": products_info,
                "total_price": order["total_price"],
                "status": order["status"],
            }
        )

    return informations
