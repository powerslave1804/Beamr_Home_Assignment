# Appium Automation Task

## Overview

This project contains a small Appium test using the Page Object Model (POM) pattern.

The test is intended to verify the following flow:

1. Start the JPEGmini Pro application.
2. Close the Trial popup.
3. Click the **Minime Mode** button.
4. Verify that the application switched to the Minime window.
5. Click the **Expand / Regular Mode** button.
6. Verify that the application returned to the Regular window.

## Project structure

```text
automation/
├── pages/
│   ├── base_page.py
│   ├── regular_page.py
│   └── minime_page.py
├── tests/
│   └── test_window_modes.py
├── conftest.py
└── README.md
```

## Page Objects

The application is split into two page objects:

* `RegularPage` - contains the locator and actions for the normal application window.
* `MinimePage` - contains the locator and actions related to Minime Mode.
* `BasePage` - contains common methods used by both pages.

The main locators found in Appium Inspector were:

* `BtnMiniMode` - Minime Mode button in the Regular window.
* `BtnNormalMode` - Expand / return to Regular Mode button in the Minime window.
* Trial popup Continue button:
  `/Window/Custom[3]/Custom[2]/Button[3]/Text`

## What was tested

The test successfully performs the first part of the flow:

* The Trial popup is found and clicked using its XPath.
* `BtnMiniMode` is found in the Regular window.
* `BtnMiniMode` is clicked and the application switches to Minime Mode.
* After switching to Minime Mode, the test tries to find `BtnNormalMode`.

The important part here is that `BtnNormalMode` could not be found through the Appium/WinAppDriver session after switching to Minime Mode.

The test therefore checks this behavior explicitly:

```python
assert not normal_button_available
```

This confirms that the locator which is visible in Appium Inspector for the Minime window is not available through the test session after the window changes.

## Problem found

The main problem was not finding the correct locator in Appium Inspector.

The locators were available there:

* `BtnMiniMode` for the Regular window
* `BtnNormalMode` for the Minime window

However, the Appium session used by pytest did not expose the Minime window in the same way.

After switching to Minime Mode, `page_source` contained only the main WPF window and did not contain `BtnNormalMode`. Attempts to find it using both its AutomationId and its XPath also failed.

The Minime window itself was visible on the desktop, but it was not available as a normal element in the current Appium/WinAppDriver UI tree.

I also checked the window handles and the window size returned by Appium. These did not provide a reliable way to access the Minime window. The reported window size stayed the same as the main application window.

## Returning to Regular Mode

The Minime window has a small Expand button at approximately `(20, 20)`.

Since Appium could not access that button as an element, I used the Windows click command as a fallback:

```python
self.driver.execute_script(
    "windows: click",
    {"x": 20, "y": 20}
)
```

This successfully returns the application to the Regular window.

However, after returning to Regular Mode, the WinAppDriver/Appium UI tree is still not refreshed reliably. Because of that, I did not add another element assertion after returning to Regular Mode that could give a false result.

## Result

The test currently verifies the part of the flow that can be reliably tested through the Appium session:

* Trial popup can be handled.
* Minime Mode button can be located and clicked.
* After switching to Minime Mode, the expected `BtnNormalMode` element is not exposed to the Appium/WinAppDriver session.
* The application can still be returned to Regular Mode using the Windows click fallback.

The remaining issue is the interaction between the Minime window and WinAppDriver. The Minime window is visible and interactive, but it is not exposed as a normal Appium UI tree in the pytest session, which prevents the final **click Expand + verify Regular Mode** step from being implemented reliably with Appium alone.
