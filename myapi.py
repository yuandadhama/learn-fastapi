from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import psycopg2

# # db setup connection
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="kaito3636", port=5432)

# # cursor to execute sql query
cur = conn.cursor()

# define the app to utilize fast api library
app = FastAPI()

# set the cors, the external source that can access this api (frontend page)
origin = "http://127.0.0.1:5500/"
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
  # when cur.execute is called, the cur now have values from the query and need to be fetched to use the values
  cur.execute("SELECT * FROM student")

  # empty data student that will be filled and returned as response 
  data_student = {}

  # loop multiple fetched data from cur
  for row in cur.fetchall():

    # fill the value of data student
    data_student[row[3]] = {
      "name": row[0],
      "age": row[1],
      "year": row[2]
    }
  
  # return data student as response
  return data_student

@app.get("/get-student/")
def get_student(id: int):
  # find the student based on the id parameter
  cur.execute("SELECT * FROM student WHERE id = %s", (str(id)))
  
  # fetch the data student from cur
  student = cur.fetchone()
  
  return {
    "name": student[0],
    "age": student[1],
    "year": student[2]
  }

@app.post("/create-student/") 
def create_student(student: Student):

  # get the highest id 
  cur.execute("SELECT MAX(id) FROM student")

  # add 1 the highest id to create new id for new student
  new_id = cur.fetchone()[0] + 1

  # insert new data to db
  cur.execute("""INSERT INTO student (name, age, year, id)
                VALUES (%s, %s, %s, %s)
              """, (student.name, student.age, student.year, new_id))
  
  # conn.commit to save changes in db
  conn.commit()
  
  # return response message
  return {"msg":"adding new student success", "isSuccess": True}
  

# @app.put("/update-student/{student_id}")
# def update_student(student_id: int, student: UpdateStudent):
#   if student_id not in students:
#     return {"Error" : "Student does not exist"}
  
#   if student.name != None:
#     students[student_id].name = student.name

#   if student.age != None:
#     students[student_id].age = student.age

#   if student.year != None:
#     students[student_id].year = student.year

#   return students[student_id]

# @app.delete("/delete-student/{student_id}")
# def delete_student(student_id: int):
#   if student_id not in students:
#     return {"error":"Student with id = {student_id} doesn't exist"}
#   del students[student_id] 
#   return {"message":"student deleted successfully"}

# conn.commit()

# cur.close()
# conn.close()