from db import HarperModel, model_field
import logging

log = logging.getLogger("gunicorn.error")


class Character(HarperModel):
    """
    Serialization is defined via functions; the idea is to provide
    validation within the function and return True on success

    The @model_field decorator is there so that when the create() method is called,
    it knows to run validation for each field and build up a valid dict to save to the DB
    """

    def __init__(self):
        # Declare the DB schema and table:
        super().__init__("dungeonmaster", "character")

        # Declare the fields that must be present when a payload is assigned:
        self.required_fields = ["name", "race", "classname"]

        # Derived fields are initialized with a default:
        self.derived_fields = {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "armor_class": 0,
            "hp": 0,
            "speed": 0,
            "darkvision": 0,
            "xp": 0,
            "str_mod": 0,
            "dex_mod": 0,
            "con_mod": 0,
            "int_mod": 0,
            "wis_mod": 0,
            "cha_mod": 0,
            "str_throw": 0,
            "dex_throw": 0,
            "con_throw": 0,
            "int_throw": 0,
            "wis_throw": 0,
            "cha_throw": 0,
        }

    def __name__(self):
        return "Character"

    def post_process(self):
        """
        This method gets called at the end of 'create' - use for additional logic before persisting
        """
        pass

    @model_field("name")
    def name(self, value):
        """
        You can put whatever validation code you want here; just make sure
        to return true for success and false for failure
        """
        return isinstance(value, str)

    @model_field("race")
    def race(self, value=None):
        allowed_values = {
            "Dragonborn": {"str_mod": 2, "speed": 30, "cha_mod": 1},
            "Hill Dwarf": {
                "speed": 25,
                "darkvision": 60,
                "con_mod": 2,
                "hp": 1,
                "wis_mod": 1,
            },
            "Mountain Dwarf": {
                "speed": 25,
                "darkvision": 60,
                "con_mod": 2,
                "str_mod": 2,
            },
            "Elf": {"speed": 30, "darkvision": 60, "dex_mod": 2,},
            "Gnome": {"speed": 25, "darkvision": 60, "int_mod": 2},
            "Half-Elf": {"speed": 30, "darkvision": 60, "cha_mod": 2},
            "Half-Orc": {"speed": 30, "darkvision": 60, "str_mod": 2, "con_mod": 1,},
            "Halfling": {"speed": 25, "dex_mod": 2},
            "Human": {"speed": 30},
            "Tiefling": {"speed": 30, "darkvision": 60, "int_mod": 1, "cha_mod": 2,},
        }

        if value not in list(allowed_values.keys()):
            return False

        selected = allowed_values[value]
        for ability in selected:
            self.derived_fields[ability] += selected[ability]

        return True

    @model_field("classname")
    def classname(self, value=None):
        allowed_values = {
            "Barbarian": {"hp": 12, "str_throw": 1, "con_throw": 1},
            "Bard": {"hp": 8, "dex_throw": 1, "cha_throw": 1},
            "Cleric": {"hp": 8, "wis_throw": 1, "cha_throw": 1},
            "Druid": {"hp": 8, "int_throw": 1, "wis_throw": 1},
            "Fighter": {"hp": 10, "str_throw": 1, "con_throw": 1},
            "Monk": {"hp": 8, "dex_throw": 1, "str_throw": 1},
            "Paladin": {"hp": 10, "wis_throw": 1, "cha_throw": 1},
            "Ranger": {"hp": 10, "str_throw": 1, "dex_throw": 1},
            "Rogue": {"hp": 8, "dex_throw": 1, "int_throw": 1},
            "Sorcerer": {"hp": 6, "con_throw": 1, "cha_throw": 1},
            "Warlock": {"hp": 8, "wis_throw": 1, "cha_throw": 1},
            "Wizard": {"hp": 6, "int_throw": 1, "wis_throw": 1},
        }

        if value not in list(allowed_values.keys()):
            return False

        selected = allowed_values[value]
        for ability in selected:
            self.derived_fields[ability] += selected[ability]

        return True

    def point_buy(self, *args):
        """
        This is an example of a method that takes an input and manipulates the model somehow

        Since there isn't a decorator specifying a model_field, this will not be added to the payload or saved in the DB
        It will however affect validation, so return True for a successful method call
        """
        ability_check = [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]

        points = args[1]

        for key in points:
            if key not in ability_check:
                return False

            self.derived_fields[key] += points[key]

        return True
