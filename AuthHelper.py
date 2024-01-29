import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_avito_search_sort_by_price(browser):
    browser.get("https://www.avito.ru")

    search_input = browser.find_element(By.CSS_SELECTOR,'input[class="input-input-Zpzc1"]')
    search_input.send_keys("лопата" + Keys.RETURN)
    time.sleep(2)


    sort_by_price_option = browser.find_element(By.CLASS_NAME,
                                                'sort-sort-klm3E')
    sort_by_price_option.click()
    time.sleep(1)
    # Выбираем опцию сортировки по возрастанию цены
    sort_by_price_option = browser.find_element(By.XPATH,  "//*[@data-marker='sort/custom-option(1)']")
    sort_by_price_option.click()

    time.sleep(2)


    price_elements = browser.find_elements(By.XPATH, "//div[@class='price']")


    prices = [int(price.text.replace(" ", "")) for price in price_elements]


    assert all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1)), "Цены расположены в неправильном порядке"