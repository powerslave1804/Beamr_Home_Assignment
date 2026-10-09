# Appium Automation Task

## Overview

This project contains a small Appium test using the Page Object Model (POM) pattern.

The test is intended to verify the following flow:

1. Start the JPEGmini Pro application.
2. Dismiss the Trial popup.
3. Click the **Minime Mode** button.
4. Verify the transition to Minime Mode.
5. Click the **Expand / Regular Mode** button.
6. Verify the return to Regular Mode.

Due to a limitation encountered with the Appium/WinAppDriver session, the complete flow could not be reliably verified.

## Project Structure

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

The application interactions are organized into three page objects:

* `RegularPage` — contains the locator and actions for the Regular window.
* `MinimePage` — contains the locator and actions related to Minime Mode.
* `BasePage` — contains common methods shared by both page objects.

The main locators identified using Appium Inspector were:

* `BtnMiniMode` — Minime Mode button in the Regular window.
* `BtnNormalMode` — Expand / return to Regular Mode button in the Minime window.
* Trial popup Continue button:

  `/Window/Custom[3]/Custom[2]/Button[3]/Text`

## What Was Tested

The test performs the following actions:

* Locates and clicks the Trial popup Continue button using its XPath.
* Locates `BtnMiniMode` in the Regular window.
* Clicks `BtnMiniMode` to initiate the transition to Minime Mode.
* Attempts to locate `BtnNormalMode` after the transition.

The test checks whether `BtnNormalMode` is available through the current Appium/WinAppDriver session. The element was not found, so the test contains the following assertion:

```python
assert not normal_button_available
```

This assertion verifies that `BtnNormalMode` was not found in the current test session. It does not establish that the element is unavailable in every Appium session or under all circumstances.

## Problem Found

The main difficulty was that the Minime window was not exposed in the same way through the pytest Appium session as it was in Appium Inspector.

After attempting to switch to Minime Mode, the `page_source` returned by the test session contained only the main WPF window and did not include `BtnNormalMode`. Attempts to locate the button using its AutomationId and an XPath locator were unsuccessful.

Although Appium Inspector identified the following elements:

* `BtnMiniMode` in the Regular window.
* `BtnNormalMode` in the Minime window.

The pytest session did not reliably expose the Minime window and its controls through the UI tree.

I also examined the window handles and the window dimensions reported by Appium. These checks did not provide a reliable way to access the Minime window, and the reported window size remained the same as that of the main application window.

## Attempt to Return to Regular Mode

The Minime window's Expand button was identified in Appium Inspector at approximately `(20, 20)`.

Since the button could not be located as an element through the pytest Appium session, I attempted to click its coordinates using the Windows click command:

```python
self.driver.execute_script(
    "windows: click",
    {"x": 20, "y": 20}
)
```

This was a fallback attempt to activate the Expand button. However, the successful return to Regular Mode was not independently confirmed, so the result of this action remains unverified.

I did not add a final element assertion because the Appium/WinAppDriver UI tree did not reliably expose the expected elements after the window transition.

## Result

The test covers the following checks and actions:

* The Trial popup Continue button is located and clicked.
* `BtnMiniMode` is located in the Regular window.
* The Minime Mode transition is initiated by clicking `BtnMiniMode`.
* `BtnNormalMode` is not found through the current Appium/WinAppDriver session after the attempted transition.
* A coordinate-based click is attempted as a fallback to activate the Expand button.

The test does not fully verify both window transitions. In particular, the return to Regular Mode has not been independently confirmed.

The main limitation encountered was the inconsistent availability of the Minime window and its controls through the Appium/WinAppDriver UI tree. As a result, the complete requested flow could not be reliably automated and verified with the current approach.
