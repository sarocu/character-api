from dotenv import load_dotenv
from db import HarperDB

load_dotenv()

database = HarperDB()
database.base_url = "http://localhost:9925"
database.migrate("init")
