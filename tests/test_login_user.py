import allure
from api_client import StellarBurgersAPI
from helpers import generate_email
from data import WRONG_PASSWORD, ERROR_MESSAGES


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        user_data = registered_user["user_data"]
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на логин"):
            response = api.login(user_data["email"], user_data["password"])
        
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert "user" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_wrong_credentials(self):
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на логин с неверными данными"):
            response = api.login(generate_email(), WRONG_PASSWORD)
        
        with allure.step("Проверка статус кода ответа (401)"):
            assert response.status_code == 401
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_MESSAGES["incorrect_credentials"]
