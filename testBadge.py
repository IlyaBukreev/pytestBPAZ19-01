import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class TestLogin:

    def setup_method(self):
        self.driver = webdriver.Chrome()

    def teardown_method(self):
        self.driver.close()

    def is_element_present(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def test_login_with_valid_credentials(self):
        self.driver.get('https://www.saucedemo.com')
        login_input = self.driver.find_element(By.ID, 'user-name')
        login_input.send_keys('standard_user')
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('secret_sauce')
        login_input.submit()

        WebDriverWait(self.driver, 10).until(
            EC.url_to_be('https://www.saucedemo.com/inventory.html')
        )

        # Найти все элементы с классом 'btn_inventory' и добавить в корзину
        add_to_cart_buttons = self.driver.find_elements(By.CLASS_NAME, 'btn_inventory')
        for button in add_to_cart_buttons:
            button.click()
            time.sleep(3)

            # Проверить изменение класса shopping_cart_badge после добавления товара
            cart_badge_elements = self.driver.find_elements(By.CLASS_NAME, 'shopping_cart_badge')
            assert len(cart_badge_elements) == 1 and cart_badge_elements[0].text != '0', "Корзина пуста после добавления товара"

        # Найти все элементы с классом 'btn_secondary' (удаление товаров) и убрать из корзины
        remove_buttons = self.driver.find_elements(By.CLASS_NAME, 'btn_secondary')
        for remove_button in remove_buttons:
            remove_button.click()
            time.sleep(3)

        try:
            shopping_cart_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "shopping_cart_link"))
            )
            # Если элемент виден, выводим сообщение об успешной проверке
            print("Элемент shopping_cart_link отображается на странице.")
        except:
            # Если элемент не найден или не виден, выводим сообщение об ошибке
            print("Корзина пауста.")

        # Убедиться, что тест успешно завершает выполнение
        self.driver.quit()

