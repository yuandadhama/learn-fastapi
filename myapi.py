from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from db import students
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
  name: str
  age: int
  year: str

class UpdateStudent(BaseModel):
  name: Optional[str] = None
  age: Optional[int] = None
  year: Optional[str] = None

@app.get("/") 
def index():
  return students

@app.get("/get-student/{student_id}")
def get_student(student_id: int):
  if student_id not in students:
    return {"error":"Student not found"}
  return students[student_id]

@app.post("/create-student/")
def create_student(student: Student):
   new_id = max(students.keys()) + 1
   students[new_id] = student
   return {new_id: students[new_id]}
  

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
  if student_id not in students:
    return {"Error" : "Student does not exist"}
  
  if student.name != None:
    students[student_id].name = student.name

  if student.age != None:
    students[student_id].age = student.age

  if student.year != None:
    students[student_id].year = student.year

  return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
  if student_id not in students:
    return {"error":"Student with id = {student_id} doesn't exist"}
  del students[student_id] 
  return {"message":"student deleted successfully"}

