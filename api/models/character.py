from db import HarperModel, model_field


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

    def __name__(self):
        return "Character"

    @model_field("name")
    def name(self, value):
        """
        You can put whatever validation code you want here; just make sure
        to return true for success and false for failure
        """
        return isinstance(value, str)

    @model_field("race")
    def race(self, value=None):
        return isinstance(value, str)

    @model_field("classname")
    def classname(self, value=None):
        return isinstance(value, str)
