import json
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, Annotated, List, Dict

app = FastAPI()


def load_dataset():
    with open("database.json", "r") as file:
        return json.load(file)


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
