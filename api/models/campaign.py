from db import HarperModel, model_field
import logging

log = logging.getLogger("gunicorn.error")


class Campaign(HarperModel):
    def __init__(self):
        super().__init__("dungeonmaster", "campaign")
        self.derived_fields["encumberance"] = "NA"

    def __name__(self):
        return "Campaign"

    def post_process(self):
        total_weight = 0
        total_capacity = self.payload["character"]["strength"] * 5.0
        for item in self.payload["current_pack"]:
            total_weight += item["weight"]

        if total_weight > total_capacity:
            self.derived_fields["encumberance"] = "encumbered"

        return True

    @model_field("character")
    def character(self, value):
        return isinstance(value, dict)

    @model_field("current_hp")
    def current_hp(self, value):
        return isinstance(value, int)

    @model_field("current_xp")
    def current_xp(self, value):
        return isinstance(value, int)

    @model_field("currently_equiped")
    def currently_equiped(self, value):
        return isinstance(value, dict)

    @model_field("current_pack")
    def current_pack(self, value):
        return isinstance(value, list)
