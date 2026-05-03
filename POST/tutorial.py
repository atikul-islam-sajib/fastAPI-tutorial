import json
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, Annotated, List, Dict, Union

app = FastAPI()


def load_dataset():
    with open("database.json", "r") as file:
        return json.load(file)

def save_dataset(data):
    with open("database.json", "w") as file:
        return json.dump(data, file, indent=4)

class Students(BaseModel):
    id: Annotated[int, Field(..., description="The ID of the student", examples=[1, 2, 3])]
    name: Annotated[str, Field(..., description="The name of the student", examples=["Lena Fischer"])]
    age: Annotated[int, Field(..., description="The age of the student", examples=[20, 21, 22])]
    email: Annotated[str, Field(..., description="The email of the student", examples=["lena.fischer@example.com"])]
    is_active: Annotated[bool, Field(..., description="Whether the student is active or not", examples=[True, False])]
    enrolled_courses: Annotated[List[int], Field(..., description="The list of courses the student is enrolled in", examples=[[101, 102]])]
    profile: Annotated[
        Dict[str, Optional[Union[str, int, float]]],
        Field(
            ...,
            description="The profile of the student",
            examples=[{"major": "Computer Science", "year": 2, "gpa": 3.7}],
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
    student_id: Optional[Annotated[
        int, Field(description="The ID of the student", examples=[1, 2, 3])
    ]]
    course_id: Optional[Annotated[
        int, Field(description="The ID of the course", examples=[101, 102, 103])
    ]]
    grade: Optional[Annotated[
        str,
        Field(description="The grade of the student in the course", examples=["A", "B", "C"],
        ),
    ]]

# Add the new information to the database -> students
@app.post("/add")
def insert_students_information(student: Students):
    existing_student_details = load_dataset()["students"]
    student_details = load_dataset()
    
    for student_detail in existing_student_details:
        if student.id == student_detail["id"]:
            raise HTTPException(
                status_code=400,
                detail="The student ID already exists in the database",
            )
            
    
    student_details["students"].append(student.model_dump())
    
    save_dataset(student_details)
    
    return student_details
        
    
# Add the grade
@app.post("/grades")
def add_new_grades(grades: Grades):
    student_grades = load_dataset()["grades"] # it would return a list of dictionaries
    
    student_grades.append(grades.model_dump())
    
    save_dataset(student_grades)
    
    return student_grades