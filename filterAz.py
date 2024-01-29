import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver():
    # Создаем экземпляр веб-драйвера перед каждым тестом
    driver = webdriver.Chrome()
    yield driver
    # Закрываем веб-драйвер после каждого теста
    driver.quit()


def test_login_and_filter_products(driver):
    # Открываем сайт
    driver.get('https://www.saucedemo.com')

    # Заполняем поле логина
    login_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'user-name'))
    )
    login_input.send_keys('standard_user')

    # Заполняем поле пароля
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'password'))
    )
    password_input.send_keys('secret_sauce')

    # Добавляем ожидание перед нажатием Enter
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'login-button'))
    )
    login_button.click()

    # Фильтрируем товары по имени (A to Z)
    filter_products(driver, 'az')

    # Получаем список названий товаров
    product_names = [element.text.lower() for element in
                     WebDriverWait(driver, 10).until(
                         EC.visibility_of_all_elements_located((By.CLASS_NAME, 'inventory_item_name'))
                     )]

    # Проверяем, что товары отсортированы в алфавитном порядке
    assert product_names == sorted(product_names), "Товары не отсортированы в алфавитном порядке"


def filter_products(driver, value):
    # Находим элемент выпадающего списка
    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'product_sort_container'))
    )

    # Используем Select для удобства работы с выпадающим списком
    select = Select(sort_dropdown)

    # Выбираем опцию по значению
    select.select_by_value(value)

    # Добавляем ожидание, чтобы дать время для обновления страницы после фильтрации
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item'))
    )
