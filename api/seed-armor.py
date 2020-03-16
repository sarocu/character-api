import csv
from dotenv import load_dotenv
from db import HarperDB
from models.equipment import Equipment

load_dotenv()

database = HarperDB()
database.base_url = "http://localhost:9925"

with open("../uploads/armor.csv", mode="r", encoding="utf-8-sig") as armor_csv:
    armor = csv.DictReader(armor_csv)
    print(armor.fieldnames)
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

    for row in armor:
        new_armor = Equipment()
        payload = {
            "name": row["name"],
            "equip_type": row["equip_type"],
            "base_cost": float(row["base_cost"]),
            "weight": int(row["weight"]),
            "base_attributes": {
                "armor_class": row["armor_class"],
                "stealth": row["stealth"],
            },
        }

        is_valid = new_armor.create(payload)
        if is_valid:
            response = database.insert(new_armor)
            print(response)
        else:
            print(is_valid)
