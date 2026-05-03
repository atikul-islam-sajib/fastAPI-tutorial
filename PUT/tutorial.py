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
    id: Optional[Annotated[int, Field(description="The ID of the student", examples=[1, 2, 3])]] = None
    name: Optional[Annotated[str, Field(description="The name of the student", examples=["Lena Fischer"])]] = None
    age: Optional[Annotated[int, Field(description="The age of the student", examples=[20, 21, 22])]] = None
    email: Optional[Annotated[str, Field(description="The email of the student", examples=["lena.fischer@example.com"])]] = None
    is_active: Optional[Annotated[bool, Field(description="Whether the student is active or not", examples=[True, False])]] = None
    enrolled_courses: Optional[Annotated[List[int], Field(description="The list of courses the student is enrolled in", examples=[[101, 102]])]] = None
    profile: Optional[Annotated[
        Dict[str, Optional[Union[str, int, float]]],
        Field(
            description="The profile of the student",
            examples=[{"major": "Computer Science", "year": 2, "gpa": 3.7}],
        ),
    ]] = None


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
    
# Update student ID
@app.put("/student")
def update_student_id(student_id: int, student: Students):
    students_detail = load_dataset() # It will return a list of dictionaries
    
    new_details = student.model_dump()
    
    for student_info in students_detail["students"]:
        if student_id == student_info["id"]:
            student_info.update(new_details)
            break
        
    
        
    save_dataset(students_detail)
    return students_detail
        
        