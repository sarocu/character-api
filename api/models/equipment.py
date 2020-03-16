from db import HarperModel, model_field
import logging

log = logging.getLogger("gunicorn.error")


class Equipment(HarperModel):
    """
    This class represents the different equipment that may be acquired throughout a campaign

    """

    def __init__(self):
        super().__init__("dungeonmaster", "equipment")

        self.required_fields = []
        self.derived_fields = {}

    def __name__(self):
        return "Equipment"

    def post_process(self):
        pass

    @model_field("name")
    def name(self, value):
        return isinstance(value, str)

    @model_field("equip_type")
    def equip_type(self, value):
        allowed_values = [
            "currency",
            "heavy-armor",
            "light-armor",
            "medium-armor",
            "shield",
            "simple-melee",
            "simple-ranged",
            "martial-melee",
            "martial-ranged",
            "ammunition",
            "arcane",
            "holy",
            "druidic",
            "container",
            "tools",
            "other",
        ]

        if value not in allowed_values:
            return False
        else:
            return True

    @model_field("base_cost")
    def base_cost(self, value):
        return isinstance(value, float)

    @model_field("base_attributes")
    def base_attributes(self, value):
        return isinstance(value, dict)

    @model_field("weight")
    def weight(self, value):
        return isinstance(value, float)
