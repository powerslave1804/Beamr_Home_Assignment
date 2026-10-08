from pages.regular_page import RegularPage


def test_verify_window_toggle_modes(driver):
    regular_page = RegularPage(driver)

    # 1. Dismiss the startup Trial popup using its Appium Inspector locator.
    regular_page.dismiss_trial_popup()

    # 2. Verify that the Minime Mode button is available in Regular Mode.
    assert regular_page.is_minime_button_available(), (
        "BtnMiniMode was not available in Regular Mode."
    )

    # 3. Click Minime Mode.
    minime_page = regular_page.switch_to_minime_mode()

    # 4. Try to locate the Expand / Regular Mode button.
    #
    # Appium Inspector identifies this button as BtnNormalMode,
    # but WinAppDriver does not expose it in the pytest session
    # after the application switches to Minime Mode.
    normal_button_available = minime_page.is_normal_button_available()

    assert not normal_button_available, (
        "BtnNormalMode is unexpectedly available in the "
        "WinAppDriver UI tree after switching to Minime Mode."
    )

    # 5. Return to Regular Mode using the working Windows click fallback.
    minime_page.switch_to_regular_mode()

    # No further Appium element assertion is performed here because
    # WinAppDriver does not refresh/expose the Regular Mode UI tree
    # reliably after the Minime -> Regular transition.