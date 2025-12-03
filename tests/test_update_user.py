import allure
from api_client import StellarBurgersAPI
from helpers import generate_email, generate_name
from data import NEW_PASSWORD, ERROR_MESSAGES


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_with_authorization(self, authorized_user):
        api = StellarBurgersAPI()
        token = authorized_user["access_token"]
        
        with allure.step("Изменение email пользователя"):
            new_email = generate_email()
            response = api.update_user({"email": new_email}, token)
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"]["email"] == new_email
        
        with allure.step("Изменение name пользователя"):
            new_name = generate_name()
            response = api.update_user({"name": new_name}, token)
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"]["name"] == new_name
        
        with allure.step("Изменение password пользователя"):
            response = api.update_user({"password": NEW_PASSWORD}, token)
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_authorization(self):
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на обновление без авторизации"):
            response = api.update_user({"email": generate_email()})
        
        with allure.step("Проверка статус кода ответа (401)"):
            assert response.status_code == 401
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_MESSAGES["should_be_authorised"]
