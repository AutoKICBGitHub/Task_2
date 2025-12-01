import allure
from api_client import StellarBurgersAPI
from helpers import delete_user, normalize_token
from data import ERROR_MESSAGES, DEFAULT_PASSWORD


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data):
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = api.register_user(user_data["email"], user_data["password"], user_data["name"])
        
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "user" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
        
        with allure.step("Удаление созданного пользователя после теста"):
            access_token = normalize_token(response_data.get("accessToken", ""))
            if access_token:
                headers = {"Authorization": f"Bearer {access_token}"}
                delete_user(headers)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, registered_user):
        user_data = registered_user["user_data"]
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на создание уже существующего пользователя"):
            response = api.register_user(user_data["email"], user_data["password"], user_data["name"])
        
        with allure.step("Проверка статус кода ответа (403)"):
            assert response.status_code == 403
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_MESSAGES["user_already_exists"]

    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_missing_field(self):
        api = StellarBurgersAPI()
        
        with allure.step("Подготовка данных без поля email"):
            user_data = {
                "password": DEFAULT_PASSWORD,
                "name": "TestUser"
            }
        
        with allure.step("Отправка запроса на создание пользователя без обязательного поля"):
            response = api.register_user(data=user_data)
        
        with allure.step("Проверка статус кода ответа (403)"):
            assert response.status_code == 403
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert ERROR_MESSAGES["required_fields"] in response_data["message"]
