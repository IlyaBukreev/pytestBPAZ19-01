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

    add_to_cart_button = driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack')
    add_to_cart_button.click()

    time.sleep(3)

    cart_badge_element = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
    assert cart_badge_element.text == '1', "Элемент корзины не отображает правильное количество товаров"

    # Добавляем переход на иконке shopping_cart_link
    shopping_cart_link = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
    shopping_cart_link.click()

    # Ожидаем загрузки страницы корзины
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'cart_item'))
    )

    # Проверяем, что на странице корзины отображается элемент с классом cart_item
    cart_item_element = driver.find_element(By.CLASS_NAME, 'cart_item')
    assert cart_item_element.is_displayed(), "Элемент cart_item не отображается на странице корзины"
