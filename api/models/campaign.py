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
        strength = self.payload["character"]["strength"]
        for item in self.payload["current_pack"]:
            total_weight += item["weight"]

        if total_weight > strength * 15.0:
            self.derived_fields["encumberance"] = "cannot-move"
        elif total_weight > strength * 10.0:
            self.derived_fields["encumberance"] = "heavily-encumbered"
        elif total_weight > strength * 5.0:
            self.derived_fields["encumberance"] = "encumbered"
        else:
            self.derived_fields["encumberance"] = "NA"

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
