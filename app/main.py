import os
import uvicorn
from typing import Union
from fastapi import Depends, FastAPI, Form
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from database.database_mongo import DatabaseMongo
from dependencies import get_token_header
from routers import device, vehicle, utils, auth
from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from typing import Annotated
import requests
import json

from idp import idp

# Database
db_host = os.environ.get("DB_HOST", "obd-dev.sensorid.it")
db_port = os.environ.get("DB_PORT", "27017")
db_name = os.environ.get("DB_NAME", "obd")
db_user = os.environ.get("DB_USER", "sensoridAdmin")
db_passwd = os.environ.get("DB_PASSWD", "10T53nsor.2010!")
# Application
app_host = os.environ.get("APP_HOST", "obd-dev.sensorid.it")
app_port = os.environ.get("APP_PORT", "8010")

db = DatabaseMongo.database_connection(f"mongodb://{db_user}:{db_passwd}@{db_host}:{db_port}/?authMechanism=DEFAULT&authSource=admin&directConnection=true", "obd")
print(f"Database Connection: {db}")


app = FastAPI()

print("- "*20)
print(f":> APP HOST: {app_host}")
print("- "*20)


class LoginData(BaseModel):
    username: str
    password: str
    # access_token: str

"""    
idp = FastAPIKeycloak(
    server_url="https://auth.sensorid.it:8443",
    client_id="obd-client",
    client_secret="d9XXWgMN1WrNnZLCy02FCh6FwebL401H",
    admin_client_secret="SK7jPsFFONklEU2pdyBDz9D3c4tsMf6b",
    realm="OBD",
    callback_uri="https://obd-dev.sensorid.it:8010/callback"
)
"""

# idp.add_swagger_config(app)
app.include_router(auth.router)
app.include_router(vehicle.router)
app.include_router(device.router)
app.include_router(utils.router)

print(idp.login_uri)


@app.get("/test")
def home():
    return "SERVER OBD CORE API SEC - OK"


@app.get("/user")  # Requires logged in
def current_users(user: OIDCUser = Depends(idp.get_current_user())):
    return user


@app.get("/callback")
def callback(session_state: str, code: str):
    print(f"SESSION STATE : {session_state}")
    print(f"CODE: {code}")
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


if __name__ == '__main__':
    uvicorn.run(app, port=int(app_port), host=app_host, ssl_keyfile="certs/SENSORID_CERT_KEY_2023.pem", ssl_certfile="certs/SENSORID_CERT_2023.pem")
