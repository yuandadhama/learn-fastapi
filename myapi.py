from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import psycopg2

# # db setup connection
def open_connection():
  return psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="1234", port=5432)

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

@app.get("/") 
def index():
  conn = open_connection()
  cur = conn.cursor()
  
  try:
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
  finally:
    cur.close()
    conn.close()

@app.get("/get-student/")
def get_student(id: int):
  conn = open_connection()
  cur = conn.cursor()
  
  try:
    # find the student based on the id parameter
    cur.execute("SELECT * FROM student WHERE id = %s", (id,))
    
    # fetch the data student from cur
    student = cur.fetchone()
    
    return {
      "name": student[0],
      "age": student[1],
      "year": student[2]
    }
  finally:
    cur.close()
    conn.close()

@app.post("/create-student/") 
def create_student(student: Student):
  conn = open_connection()
  cur = conn.cursor()
  
  try:
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
  finally:
    cur.close()
    conn.close()
    

@app.put("/update-student/")
def update_student(id: int, student: Student):
  conn = open_connection()
  cur = conn.cursor()
  
  try:
    cur.execute("""UPDATE student SET 
                name = %s,
                age = %s,
                year = %s 
                WHERE id = %s;""", (student.name, student.age, student.year, id))
    
    conn.commit()
    return {
      "isSuccess": True,
      "msg": "successfully edit student"
    }
  except TypeError:
    return {
      "isSuccess": False,
      "msg": "something went wrong"
    }
  finally:
    cur.close()
    conn.close()
  
@app.delete("/delete-student/")
def delete_student(id: int):
  conn = open_connection()
  cur = conn.cursor()
  
  try:
    # delete student query
    cur.execute("DELETE FROM student WHERE id = %s", (id,))
    conn.commit()
    return {
      "msg": "delete student success",
      "isSuccess": True
    }
  except:
    return {
      "msg":"something went wrong",
      "isSuccess": False
    }
  finally:
    conn.close()
    cur.close()

