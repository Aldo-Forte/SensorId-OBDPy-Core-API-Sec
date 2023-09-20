from fastapi import APIRouter, Depends
from idp import OIDCUser, idp
from pydantic import BaseModel
import requests
import json

router = APIRouter(
    prefix="/auth",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

class LoginData(BaseModel):
    username: str
    password: str

class RefreshToken(BaseModel):
    token: str

@router.post("/login")
def login(login_data: LoginData):
    print(f"USERNAME: {login_data.username}")
    print(f"PASSWORD: {login_data.password}")
    login_url = "https://auth.sensorid.it:8443/realms/OBD/protocol/openid-connect/token"
    headers = {"grant_type": "password", "client_id": "obd-client"}

    data = {
        "client_id": "obd-client", 
        "client_secret": "d9XXWgMN1WrNnZLCy02FCh6FwebL401H",
        "grant_type": "password", 
        "scope": "openid",
        "username": login_data.username, 
        "password": login_data.password
        }

    response = requests.post(login_url, headers=headers, data=data)
    access_token = idp.admin_token
    print(idp.admin_token)
    print(response.text)
    response_json = json.loads(response.text)
    return response_json


@router.post("/refresh_token")
def refresh_token(refresh_token: RefreshToken):

    login_url = "https://auth.sensorid.it:8443/realms/OBD/protocol/openid-connect/token"
    headers = {"grant_type": "refresh_token", "client_id": "obd-client"}

    data = {
        "client_id": "obd-client", 
        "client_secret": "d9XXWgMN1WrNnZLCy02FCh6FwebL401H",
        "grant_type": "refresh_token", 
        "scope": "openid",
        "refresh_token" : refresh_token.token
        }

    response = requests.post(login_url, headers=headers, data=data)
    access_token = idp.admin_token
    print(idp.admin_token)
    print(response.text)
    response_json = json.loads(response.text)
    return response_json

@router.get("/user")  # Requires logged in
def current_users(user: OIDCUser = Depends(idp.get_current_user())):
    return user