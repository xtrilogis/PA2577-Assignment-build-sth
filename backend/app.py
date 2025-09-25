import os
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://web-frontend:3000"], # "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint to test connection to backend."""
    return {"message": "Successful connection to backend!"} 


@app.get("/test/items/random")
def dev_random():
    """Development endpoint for the random item endpoint."""
    return {"data": [1,"Apple","kg",3]}


@app.get("/test/items/all")
def dev_all():
    """Development endpoint for the all items endpoint."""
    return {"data": [(1,"Apple","kg",3), (2,"Banana","kg",1.5)]}


@app.get("/items/random")
def get_random_item():
    try:
        conn: psycopg2.extensions.connection = get_connection()
        curr = conn.cursor()
        curr.execute("SELECT * FROM grocery_items ORDER BY RANDOM() LIMIT 1;")
        data = curr.fetchone()
        print(data)
        # print(f"Connection to PostgreSQL established successfully. Sample data: {data}")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        data = e

    if data:
        return {"data": data}
    else:
        return {"error": f"Error fetching data: {data}"}
    

@app.get("/items/all")
def get_all_items():
    """Fetches all grocery items from the PostgreSQL database."""
    try:
        conn: psycopg2.extensions.connection = get_connection()
        curr = conn.cursor()
        curr.execute("SELECT * FROM grocery_items;")
        data = curr.fetchall()
        print(data)

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        data = e

    if data:
        return {"data": data}
    else:
        return {"error": f"Error fetching data: {data}"}
    

def get_connection() -> psycopg2.extensions.connection:
    """Establishes and returns a connection to the PostgreSQL database.
    :return: psycopg2 connection object
    :raises Exception: if connection fails
    """
    conn = psycopg2.connect(
        database=os.getenv('POSTGRES_DB', "default_db"),
        user=os.getenv('POSTGRES_USER', "default_user"),
        password=os.getenv('POSTGRES_PASSWORD', "DefaultPassword123"),
        host=os.getenv('POSTGRES_HOST', "postgres-svc"),
        port=os.getenv('POSTGRES_PORT', 5432),
    )
    return conn
