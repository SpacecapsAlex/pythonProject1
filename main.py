from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values
from pydantic import BaseModel
import traceback

config = dotenv_values(".env")

connect = psycopg2.connect(
    host=config['HOST'],
    port=config['PORT'],
    user=config['USER_ID'],
    password=config['USER_PD'],
    database=config['DB_NAME'],
)

cursor = connect.cursor()

app = FastAPI()

class vm_get_workers(BaseModel):
    id: int
    firstName: str
    position: str
    phone: str


class vm_get_worker(BaseModel):
    id: int
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: float
    departmentName: str


@app.get("/")
def root():
    return {"message": "Start Server"}


@app.get("/get-workers")
def get_workers():
    try:
        cursor.execute("""
            SELECT id, firstName, position, phone
            FROM worker;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append(vm_get_workers(
                id=worker[0],
                firstName=worker[1],
                position=worker[2],
                phone=worker[3]
            ))

        return {"workers": list_workers}
    except:
        return {"error": traceback.format_exc()}


@app.get("/get-worker/{worker_id}")
def get_worker(worker_id: int):
    try:
        cursor.execute(f"""
            SELECT w.id, w.firstName, w.surName, w.email, w.phone, w.address, w.position, w.salary, d.name
            FROM worker w
            LEFT JOIN department d ON w.department_id = d.id
            WHERE w.id = {worker_id};
        """)
        result = cursor.fetchone()
        worker = vm_get_worker(
            id=result[0],
            firstName=result[1],
            surName=result[2],
            email=result[3],
            phone=result[4],
            address=result[5],
            position=result[6],
            salary=result[7],
            departmentName=result[8]
        )
        return {"worker": worker}
    except:
        return {"error": traceback.format_exc()}

