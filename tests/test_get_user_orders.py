import allure
from api_client import StellarBurgersAPI
from data import ERROR_MESSAGES


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized_user(self, authorized_user):
        api = StellarBurgersAPI()
        token = authorized_user["access_token"]
        
        with allure.step("Отправка запроса на получение заказов"):
            response = api.get_user_orders(token)
        
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized_user(self):
        api = StellarBurgersAPI()
        
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = api.get_user_orders()
        
        with allure.step("Проверка статус кода ответа (401)"):
            assert response.status_code == 401
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == ERROR_MESSAGES["should_be_authorised"]
