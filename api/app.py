import os
import io
import logging
import uuid
from flask import Flask, request, send_file
from flask_restx import Api, Resource
from dotenv import load_dotenv, find_dotenv

from decorators import require_key

load_dotenv(find_dotenv())

app = Flask(__name__)
rest = Api(app)

debug = os.environ.get("DEBUG")

class Resource(Resource):
    """
    Require that all resources apply the bearer token authentication
    """

    method_decorators = [require_key]

@rest.route("/character")
class CharacterCRUD(Resource):
    def get(self):
        _id = request.args.get("id")
        return {"name":"Marty McFly", "id":_id}

    def post(self):
        _id = str(uuid.uuid4())
        return {"id":_id, "msg":"success"}