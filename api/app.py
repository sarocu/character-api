import os
import io
import logging
from flask import Flask, request, send_file
from flask_restx import Api, Resource
from dotenv import load_dotenv, find_dotenv

from decorators import require_key
from models.character import Character
from models.equipment import Equipment
from models.campaign import Campaign

from db import HarperDB

load_dotenv(find_dotenv())

app = Flask(__name__)
rest = Api(app)
hdb = HarperDB()

debug = os.environ.get("DEBUG")
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


class Resource(Resource):
    """
    Require that all resources apply the bearer token authentication
    """

    method_decorators = [require_key]


@rest.route("/character")
class CharacterCRUD(Resource):
    def get(self):
        _id = request.args.get("id")
        character = Character()
        try:
            character.payload = hdb.get(character, _id)
            return character.payload
        except Exception as error:
            gunicorn_logger.error(error)
            return "Could not retrieve character", 400

    def post(self):
        new_character = Character()
        valid = new_character.create(request.json)
        if valid:
            response = hdb.insert(new_character)
            return {
                "id": new_character._id,
                "status": response,
                "character": new_character.payload,
            }
        else:
            return "Could not create Character", 400


@rest.route("/equipment")
class EquipmentCRUD(Resource):
    def get(self):
        _id = request.args.get("id")
        equip = Equipment()
        try:
            equip.payload = hdb.get(equip, _id)
            return equip.payload
        except Exception as error:
            gunicorn_logger.error(error)
            return "Could not retrieve equipment", 400

    def post(self):
        new_equipment = Equipment()
        valid = new_equipment.create(request.json)
        if valid:
            response = hdb.insert(new_equipment)
            return {
                "id": new_equipment._id,
                "status": response,
                "equipment": new_equipment.payload,
            }
        else:
            return "Could not create equipment", 400


@rest.route("/equipment-library")
class EquipmentLibrary(Resource):
    def get(self):
        equip_type = request.args.get("equip_type")
        try:
            response = hdb.get_list(Equipment(), equip_type, "equip_type")
            return {"equipment": response}
        except Exception as error:
            gunicorn_logger.error(error)
            return "Could not retrieve equipment", 400


@rest.route("/campaign")
class CampaignCRUD(Resource):
    def get(self):
        _id = request.args.get("id")
        try:
            response = hdb.get(Campaign(), _id)
            return {"campaign": response}
        except Exception as error:
            gunicorn_logger.error(error)
            return "Could not retrieve campaign", 400

    def post(self):
        character_id = request.args.get("character")
        try:
            character = hdb.get(Character(), character_id)
            game = Campaign()
            payload = {
                "character": character,
                "current_hp": character["hp"],
                "current_xp": character["xp"],
                "currently_equiped": {},
                "current_pack": [],
            }
            gunicorn_logger.warning(payload)
            valid = game.create(payload)
            if valid:
                response = hdb.insert(game)
                return {"campaign": game.payload}
            else:
                return "Could not create campaign: request not valid", 400
        except Exception as error:
            gunicorn_logger.error(error)
            return "Could not create campaign", 400

    def put(self):
        pass
