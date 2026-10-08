import time

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.minime_page import MinimePage


class RegularPage(BasePage):

    # Button available in Regular Mode.
    # Clicking it switches the application to Minime Mode.
    MINIME_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "BtnMiniMode"
    )

    # Trial popup Continue button discovered with Appium Inspector.
    TRIAL_CONTINUE_BUTTON = (
        AppiumBy.XPATH,
        "/Window/Custom[3]/Custom[2]/Button[3]/Text"
    )

    def dismiss_trial_popup(self):
        """
        Clicks the Continue button on the startup trial popup.
        """
        self.click_element(self.TRIAL_CONTINUE_BUTTON)
        time.sleep(1)

    def is_minime_button_available(self):
        """
        Checks whether the Regular Mode Minime button
        is available in the current Appium UI context.
        """
        return self.is_element_available(self.MINIME_BUTTON)

    def switch_to_minime_mode(self):
        """
        Switches the application from Regular Mode to Minime Mode.
        """
        self.click_element(self.MINIME_BUTTON)

        time.sleep(2)

        return MinimePage(self.driver)