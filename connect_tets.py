import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

USER = os.getenv("MYSQL_USER")
PWD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("MYSQL_PORT")
DB = os.getenv("MYSQL_DB")

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

with engine.connect() as conn:
    print(conn.execute(text("SELECT DATABASE();")).scalar())
    print(conn.execute(text("SELECT VERSION();")).scalar())
    rows = conn.execute(text("SELECT 1 AS ok")).fetchall()
    print(rows)