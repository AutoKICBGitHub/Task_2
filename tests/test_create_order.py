import allure
from api_client import StellarBurgersAPI
from helpers import get_ingredient_ids
from data import EXAMPLE_INGREDIENT_IDS, INVALID_INGREDIENT_HASH, ERROR_MESSAGES


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_authorization(self, authorized_user):
        api = StellarBurgersAPI()
        token = authorized_user["access_token"]
        
        with allure.step("Получение списка ингредиентов"):
            ingredient_ids = get_ingredient_ids(2)
        
        with allure.step("Отправка запроса на создание заказа"):
            response = api.create_order(ingredient_ids, token)
        
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self):
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = api.create_order([EXAMPLE_INGREDIENT_IDS[0]])
        
        with allure.step("Проверка статус кода ответа (400)"):
            assert response.status_code == 400
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authorized_user):
        api = StellarBurgersAPI()
        token = authorized_user["access_token"]
        
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = api.create_order([], token)
        
        with allure.step("Проверка статус кода ответа (400)"):
            assert response.status_code == 400
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_MESSAGES["ingredient_ids_required"]

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, authorized_user):
        api = StellarBurgersAPI()
        token = authorized_user["access_token"]
        
        with allure.step("Отправка запроса на создание заказа с неверным хешем"):
            response = api.create_order([INVALID_INGREDIENT_HASH], token)
        
        with allure.step("Проверка статус кода ответа (500)"):
            assert response.status_code == 500
