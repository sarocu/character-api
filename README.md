# Character Creator API
A simple python API for the Character Creator project - a goofy little toy project for AWS and Azure research. It implements a DnD character creator.

## Local Usage
This project is built using python 3.7 - set up an appropriate interpreter first. Then create a virtualenv and install dependencies, including this one:
```bash
python3.7 -m venv character

# cd into the project directory:
cd ...
pip install -r requirements.txt

# If you want local changes to get picked up by python, link the source to the virtualenv package:
pip install -e .
```
## Git Hooks
`pre-commit` is used to run Git hooks for various things like keeping dependencies up to date.

Get setup by running: `pre-commit install`

You can run the pre-commit scripts against all files in the repo with a `pre-commit run --all-file`

`black` is setup for a pre-commit hook to enforce PEP8 guidelines for the project. It can be run outside of the hook with a `black .`

## Keeping Up to Date
```bash
# check for out of date packages:
pip list --outdated

# upgrade individual packages:
pip install --upgrade django

# upgrade everything that needs it (pip > 20.0.x):
pip list --format freeze --outdated | sed 's/=.*//g' | xargs -n1 pip install -U
```

## Authentication
This is only a toy API so the authentication is simple - just a bearer token. A decorator is applied to all routes in the Flask App to enforce it's use. Create a new token, add it to the .env, start the docker services, and make sure it's included in all the REST requests. 

When deploying make sure its set as an environment variable on the Azure Container Instance or AWS ECS.

Generate a key as follows:
```python
import uuid

key = uuid.uuid4() # generate a random 128 bit UUID
str(key) # cast to string and paste into the .env files
```

## Docker and Running in Production
The Flask API is Dockerized so that the weather package is installed into the container and Gunicorn creates a socket that responds to requests. The goal with this is to run the Flask API using a container service and not to directly expose it to public HTTP. The network flow would go:
```bash
user HTTP request -> VPC Subnet -> ECS/Fargate -> Gunicorn -> Flask API
```

For the weather service to be installed correctly, the requirements.txt file should **not** install the package, rather the Dockerfile copies the package to a directory in the container and installs it with a
```bash
pip install -e .
```

Nominally, the app is running on port 8000 inside the container, and Docker-Compose maps it to 8000 on the host. This is arbitrary.

### Fargate
In production, the API is hosted in a Docker container on AWS Fargate - a service for abstracting EC2 management away from using the container service. A cluster of containers using the Docker image is managed by AWS according to load (each container gets a set memory and CPU credit limit) as defined by a task definition.

In addition to specifying memory and CPU limits, the task definition is used to pass environment variables to the Docker container and the specify the startup of the container using Docker commands and entrypoints. For the Weather service, specify the entrypoint as:
```bash
sh,-c
```
And the command as (same as the docker-compose file):
```bash
/usr/local/bin/supervisord -c /gunicorn/supervisord.conf
```

## Pushing to the Container Registry
The Docker image needs to be registered with the EC2 Container Registry for the ECS container to draw from.

### Requirements
* AWS CLI
* a IAM user with ECR permissions set

In a command line, run:
```bash
aws ecr get-login --region us-west-2 --no-include-email
# output is a command to get an auth token, takes the form
# docker login -u AWS -p xxxxxx https://...
# Paste the command into the terminal to create a temporary token (expires after 12 hours)

# Retrieve the token and set as an environment variable:
TOKEN=$(aws ecr get-authorization-token --output text --query 'authorizationData[].authorizationToken')

# find the correct image:
docker images

# using the image ID and the URI in the container registry, tag and push the image:
docker tag 07b905gefb14 xxxxxxx.dkr.ecr.us-west-2.amazonaws.com/api-service
docker push xxxxxx.dkr.ecr.us-west-2.amazonaws.com/api-service
```

# HarperDB Migrations
`db.py` serves as the connector to Harper in order to perform CRUD operations and migrations on the DB. Migrations are used to programmatically describe the structure of the database and changes; simple YAML files are used to configure a migration. 

| Command | Description | Required Subcommands |
|---------|-------------|----------------------|
| `init` | Used to define the initial DB schemas and tables | `schema`, `table` |

| Subcommand | Description | Required Params |
|------------|-------------|-----------------|
| `schemas` | Lists of schemas to create | `name` |
| `table` | Creates a new DB table | `name`, `schema`, `attibutes` |
