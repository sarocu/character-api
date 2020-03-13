from dotenv import load_dotenv
from db import HarperDB

load_dotenv()

database = HarperDB()
database.migrate('init')