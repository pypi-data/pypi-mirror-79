from .base import BaseTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MagentoTestCase(BaseTestCase):
    def visit_product_page(self, sku):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='search']")))
        search_input.send_keys(sku)
        search_input.submit()
        pdp = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-info-main']")))

        return pdp

    def checkout_loader(self):
        driver = self.driver
        # function wait for checkout loader
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        loading = wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading-mask']")))

        return loading

    def login_page(self):
        driver = self.driver
        # function to go to login page
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        loading = wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading-mask']")))
        loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='header-my-account']")))
        loginBtn.click()

    def login(self, username, password):
        driver = self.driver
        # function to fill login form
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        login_form = wait.until(EC.visibility_of_element_located((By.XPATH, "//form[@id='login-form']")))
        email_field = driver.find_element_by_xpath("//input[@id='customer-email']")
        password_field = driver.find_element_by_xpath("//input[@id='pass']")
        email_field.send_keys(username)
        password_field.send_keys(password)
        password_field.submit()