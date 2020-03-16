import csv
from dotenv import load_dotenv
from db import HarperDB
from models.equipment import Equipment

load_dotenv()

database = HarperDB()
database.base_url = "http://localhost:9925"

with open("../uploads/weapons.csv", mode="r", encoding="utf-8-sig") as weapons_csv:
    weapons = csv.DictReader(weapons_csv)
    print(weapons.fieldnames)
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

    for row in weapons:
        new_equip = Equipment()
        payload = {
            "name": row["name"],
            "equip_type": row["equip_type"],
            "base_cost": float(row["base_cost"]),
            "weight": int(row["weight"]),
            "base_attributes": {
                "damage": row["damage"],
                "damage_type": row["damage_type"],
                "properties": row["properties"],
                "range": row["range"],
                "hands": row["hands"],
            },
        }

        is_valid = new_equip.create(payload)
        if is_valid:
            response = database.insert(new_equip)
            print(response)
        else:
            print(is_valid)
