import pytest
from appium import webdriver
from appium.options.windows import WindowsOptions

@pytest.fixture(scope="function")
def driver():
    options = WindowsOptions()
    options.app = r"C:\Users\Korisnik\AppData\Local\JpegminiPro4\JPEGminiPro.exe"
    options.set_capability("ms:experimental-webdriver", True)
    
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()
