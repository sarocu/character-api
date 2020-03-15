import os
import io
import logging
from flask import Flask, request, send_file
from flask_restx import Api, Resource
from dotenv import load_dotenv, find_dotenv

from decorators import require_key
from models.character import Character
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
