import csv
from dotenv import load_dotenv
from db import HarperDB
from models.equipment import Equipment

load_dotenv()

database = HarperDB()
database.base_url = "http://localhost:9925"

with open("../uploads/other.csv", mode="r", encoding="utf-8-sig") as other_csv:
    other = csv.DictReader(other_csv)
    print(other.fieldnames)
    # This should be the general format:
    # {
    # 	"name":"Padded Armor",
    # 	"equip_type":"light-armor",
    # 	"base_cost":5,
    # 	"weight":8,
    # 	"base_attributes":{
    # 		"armor_class":11,
    # 		"stealth":"disadvantage"
    # 	}
    # }

    for row in other:
        new_equip = Equipment()
        payload = {
            "name": row["name"],
            "equip_type": row["equip_type"],
            "base_cost": float(row["base_cost"]),
            "weight": float(row["weight"]),
        }

        is_valid = new_equip.create(payload)
        if is_valid:
            response = database.insert(new_equip)
            print(response)
        else:
            print(is_valid)
