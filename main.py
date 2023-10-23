from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values
from pydantic import BaseModel

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


@app.get("/")
def root():
    return {"message": "Start Server"}


@app.get("/get-workers")
def get_workers():
    try:
        cursor.execute("""
            SELECT firstName, position, phone
            FROM worker;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append({
                "firstName": worker[0],
                "position": worker[1],
                "phone": worker[2]
            })

        return {"workers": list_workers}
    except Exception as e:
        return {"error": e}

