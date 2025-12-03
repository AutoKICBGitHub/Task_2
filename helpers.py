import random
import string


BASE_URL = "https://stellarburgers.education-services.ru/api"


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_email():
    return f"test_{generate_random_string()}@yandex.ru"


def generate_name():
    return f"TestUser_{generate_random_string()}"


def delete_user(headers):
    try:
        from api_client import StellarBurgersAPI
        api = StellarBurgersAPI()
        token = headers.get("Authorization", "").replace("Bearer ", "")
        api.delete_user(token)
    except Exception:
        pass


def get_ingredient_ids(count=2):
    from api_client import StellarBurgersAPI
    api = StellarBurgersAPI()
    ingredients_response = api.get_ingredients()
    assert ingredients_response.status_code == 200
    ingredients_data = ingredients_response.json()
    
    if isinstance(ingredients_data, list) and len(ingredients_data) >= count:
        return [ingredients_data[i]["_id"] for i in range(count)]
    elif isinstance(ingredients_data, dict) and "data" in ingredients_data and len(ingredients_data["data"]) >= count:
        return [ingredients_data["data"][i]["_id"] for i in range(count)]
    else:
        from data import EXAMPLE_INGREDIENT_IDS
        return EXAMPLE_INGREDIENT_IDS[:count]


def normalize_token(token):
    if token and token.startswith("Bearer "):
        return token.replace("Bearer ", "")
    return token
