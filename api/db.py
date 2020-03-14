import requests
import os
import yaml
from functools import wraps
import logging
import uuid

log = logging.getLogger("gunicorn.error")


class HarperDB:
    def __init__(self):
        self.base_url = os.environ.get("DB_URI")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASSWORD")
        self.auth = (self.user, self.password)

    def migrate(self, migration):
        """
        Apply pending migrations to the DB
        """
        migration_file = os.path.join(
            os.path.dirname(__file__), "migrations", migration + ".yaml"
        )
        try:
            with open(migration_file, "r") as migration_yaml:
                migration_object = yaml.load(migration_yaml)
            self.dispatch(migration_object)
        except Exception as error:
            print(error)

    def create_schema(self, schemas):
        for schema_name in schemas:
            payload = {"operation": "create_schema", "schema": schema_name}
            try:
                response = requests.post(self.base_url, json=payload, auth=self.auth)
                response.raise_for_status()
                print("successfully created {}".format(schema_name))
            except requests.exceptions.HTTPError as error:
                print(error)

    def create_table(self, tables):
        for table_name in tables:
            payload = {
                "operation": "create_table",
                "schema": tables[table_name]["schema"],
                "table": table_name,
                "hash_attribute": tables[table_name]["attributes"],
            }
            try:
                response = requests.post(self.base_url, json=payload, auth=self.auth)
                response.raise_for_status()
                print("successfully created {}".format(table_name))
            except requests.exceptions.HTTPError as error:
                log.error(error)
                print(error)

    def insert(self, model_instance):
        """
        Perform an insert request to HDB:
            - the model_instance should have already called the 'create' method
            - the payload and fields attributes will be used in the request body
            - this will fail if the model instance isn't valid
        """
        if model_instance.valid is False:
            log.error(model_instance.payload)
            return "Can't create: Invalid Model"

        payload = {
            "operation": "insert",
            "schema": model_instance.schema,
            "table": model_instance.table,
            "records": [model_instance.payload],
        }
        try:
            response = requests.post(self.base_url, json=payload, auth=self.auth)
            response.raise_for_status()
            return {
                "response": "successfully created new {}".format(
                    model_instance.__name__()
                )
            }
        except requests.exceptions.HTTPError as error:
            log.error(error)
            log.error(payload)
            return {"response": "error - could not persist"}

    def dispatch(self, migration):
        """
        Dispatch method for performing migrations
        """
        dispatch_table = {
            "schemas": self.create_schema,
            "tables": self.create_table,
        }

        for step in migration.keys():
            print("executing {}".format(step))
            for action in migration[step].keys():
                print("dispatching {}".format(action))
                dispatch_table.get(action)(migration[step][action])


class HarperModel:
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.fields = []
        self.valid = True
        self.payload = {}
        self.required_fields = []
        self._id = str(uuid.uuid4())
        self.payload["id"] = self._id

    def __name__(self):
        return "HarperModel"

    def create(self, payload):
        """
        First check that the payload contains valid data by running it through the model validator functions
        Second, build up a dict to make a SQL insert with (fields not tagged as model fields don't get persisted)
        Finally, check that all required fields are in provided
        """
        for key in payload:
            logging.error(key)
            logging.error(payload[key])
            try:
                validate_function = getattr(self, key)
                self.valid = validate_function(self, payload[key])
                self.payload[key] = payload[key]
            except AttributeError as error:
                log.warning(error)
                log.warning("encountered unexpected key, continuing")
                continue

        for field in self.required_fields:
            if field not in self.fields:
                self.valid = False
                log.error("Missing required fields!")
                log.error("Fields Provided:")
                log.error(self.fields)
                log.error("Required Fields:")
                log.error(self.required_fields)

        return self.valid


def model_field(field_name):
    """
    This decorator is a helper for creating simple models in Harper DB
    """

    def decorator(field_validator):
        def wrapper(self, *args, **kwargs):
            self.fields.append(field_name)
            return field_validator(*args, **kwargs)

        return wrapper

    return decorator
