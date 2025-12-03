import requests
from helpers import BASE_URL


class StellarBurgersAPI:
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def _get_headers(self, token=None):
        if token:
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    def register_user(self, email=None, password=None, name=None, data=None):
        try:
            if data is None:
                data = {"email": email, "password": password, "name": name}
            return requests.post(f"{self.base_url}/auth/register", json=data)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при регистрации пользователя: {e}")
    
    def login(self, email, password):
        try:
            data = {"email": email, "password": password}
            return requests.post(f"{self.base_url}/auth/login", json=data)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при логине: {e}")
    
    def update_user(self, update_data, token=None):
        try:
            headers = self._get_headers(token)
            return requests.patch(f"{self.base_url}/auth/user", json=update_data, headers=headers)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при обновлении пользователя: {e}")
    
    def delete_user(self, token):
        try:
            headers = self._get_headers(token)
            return requests.delete(f"{self.base_url}/auth/user", headers=headers)
        except requests.exceptions.RequestException:
            pass
    
    def create_order(self, ingredients, token=None):
        try:
            data = {"ingredients": ingredients}
            headers = self._get_headers(token)
            return requests.post(f"{self.base_url}/orders", json=data, headers=headers)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при создании заказа: {e}")
    
    def get_user_orders(self, token=None):
        try:
            headers = self._get_headers(token)
            return requests.get(f"{self.base_url}/orders", headers=headers)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при получении заказов: {e}")
    
    def get_ingredients(self):
        try:
            return requests.get(f"{self.base_url}/ingredients")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при получении ингредиентов: {e}")

