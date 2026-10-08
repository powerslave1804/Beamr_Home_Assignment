from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def click_element(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def is_element_available(self, locator):
        """
        Checks whether an element can be found in the current
        Appium/WinAppDriver UI context.
        """
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False