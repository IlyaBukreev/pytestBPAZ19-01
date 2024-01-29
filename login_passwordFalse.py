import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login_with_valid_credentials(self):
        # Открываем сайт
        self.driver.get('https://www.saucedemo.com')

        # Заполняем поле логина
        login_input = self.driver.find_element(By.ID, 'user-name')
        login_input.send_keys('standard_user')

        # Заполняем поле пароля
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('secret_sauce1')

        # Добавляем ожидание перед нажатием Enter
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-button'))
        )

        # Нажимаем Enter, чтобы выполнить вход
        login_input.submit()

        try:
            # Проверяем, что успешно авторизовались
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be('https://www.saucedemo.com/inventory.html')
            )

            # Выводим сообщение об успешной аутентификации в результат теста
            print("Аутентификация успешна!")

        except Exception as e:
            # Выводим сообщение об ошибке в результат теста
            print("Ошибка при аутентификации:", str(e))

if __name__ == '__main__':
    unittest.main()
