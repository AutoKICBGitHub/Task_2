import pytest
from helpers import generate_email, generate_name, delete_user, normalize_token
from api_client import StellarBurgersAPI
from data import DEFAULT_PASSWORD


@pytest.fixture
def user_data():
    return {
        "email": generate_email(),
        "password": DEFAULT_PASSWORD,
        "name": generate_name()
    }


@pytest.fixture
def registered_user(user_data):
    api = StellarBurgersAPI()
    response = api.register_user(user_data["email"], user_data["password"], user_data["name"])
    
    access_token = ""
    refresh_token = ""
    if response.status_code == 200:
        response_data = response.json()
        access_token = normalize_token(response_data.get("accessToken", ""))
        refresh_token = response_data.get("refreshToken", "")
    
    yield {
        "user_data": user_data,
        "response": response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        delete_user(headers)


@pytest.fixture
def authorized_user(registered_user):
    user_data = registered_user["user_data"]
    api = StellarBurgersAPI()
    login_response = api.login(user_data["email"], user_data["password"])
    login_data = login_response.json()
    access_token = normalize_token(login_data.get("accessToken", ""))
    refresh_token = login_data.get("refreshToken", "")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    yield {
        "user_data": user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "headers": headers
    }
    
    delete_user(headers)
