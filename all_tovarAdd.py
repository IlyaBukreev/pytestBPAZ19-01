import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_login_with_valid_credentials(driver):
    driver.get('https://www.saucedemo.com')
    login_input = driver.find_element(By.ID, 'user-name')
    login_input.send_keys('standard_user')
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys('secret_sauce')
    login_input.submit()

    WebDriverWait(driver, 10).until(
        EC.url_to_be('https://www.saucedemo.com/inventory.html')
    )

    # Найти все элементы с указанным классом
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, 'btn_inventory')

    # Нажать на каждый элемент
    for button in add_to_cart_buttons:
        button.click()
        time.sleep(3)

    cart_badge_element = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')

    # Проверить количество товаров в значке корзины
    assert cart_badge_element.text == str(
        len(add_to_cart_buttons)), "Элемент корзины не отображает правильное количество товаров"
