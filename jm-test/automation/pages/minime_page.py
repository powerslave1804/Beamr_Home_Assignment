import time

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class MinimePage(BasePage):

    # Button used by the application to return to Regular Mode.
    NORMAL_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "BtnNormalMode"
    )

    def is_normal_button_available(self):
        """
        Checks whether the Expand / Regular Mode button is exposed
        through the current Appium/WinAppDriver UI context.
        """
        return self.is_element_available(self.NORMAL_BUTTON)

    def switch_to_regular_mode(self):
        """
        Returns the application from Minime Mode to Regular Mode.

        WinAppDriver does not reliably expose BtnNormalMode through
        the accessibility tree after the application switches to
        Minime Mode.

        Appium Inspector showed the Expand button at approximately
        (20, 20), so the Windows click command is used as a fallback.
        """
        self.driver.execute_script(
            "windows: click",
            {
                "x": 20,
                "y": 20
            }
        )

        time.sleep(2)

        from pages.regular_page import RegularPage
        return RegularPage(self.driver)