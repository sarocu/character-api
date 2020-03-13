import requests
import os
import yaml
from functools import wraps
import logging

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
        migration_file = os.path.join(os.path.dirname(__file__), 'migrations', migration + '.yaml')
        try:
            with open(migration_file, 'r') as migration_yaml:
                migration_object = yaml.load(migration_yaml)
            self.dispatch(migration_object)
        except Exception as error:
            print(error)

    def create_schema(self, schemas):
        for schema_name in schemas:
            payload = {
                "operation":"create_schema",
                "schema":schema_name
                }
            try:
                response = requests.post(self.base_url, json=payload, auth=self.auth)
                response.raise_for_status()
                print('successfully created {}'.format(schema_name))
            except requests.exceptions.HTTPError as error:
                print(error)

    
    def create_table(self, tables):
        for table_name in tables:
            payload = {
                "operation": "create_table",
                "schema":tables[table_name]['schema'],
                "table":table_name,
                "hash_attribute":tables[table_name]['attributes']
            }
            try:
                response = requests.post(self.base_url, json=payload, auth=self.auth)
                response.raise_for_status()
                print('successfully created {}'.format(table_name))
            except requests.exceptions.HTTPError as error:
                print(error)

    def insert(self, model, payload):
        pass

    def dispatch(self, migration):
        """
        Dispatch method for performing migrations
        """
        dispatch_table = {
            "schemas":self.create_schema,
            "tables":self.create_table,
        }

        for step in migration.keys():
            print('executing {}'.format(step))
            for action in migration[step].keys():
                print('dispatching {}'.format(action))
                dispatch_table.get(action)(migration[step][action])

class HarperModel:
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.fields = []
        self.valid = True
        self.payload = {}

    def create(self, payload):
        self.payload = payload
        for key in payload:
            logging.error(key)
            logging.error(payload[key])
            validate_function = getattr(self, key)
            self.valid = validate_function(self, payload[key])
        return self.fields
    
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
