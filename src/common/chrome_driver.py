from fake_useragent import UserAgent
from selenium.webdriver import Chrome, ChromeOptions


def get_chrome_driver() -> Chrome:
    ua = UserAgent()
    random_user_agent = ua.random
    options = ChromeOptions()
    options.add_argument(f"user-agent={random_user_agent}")
    # chrome_options.add_argument("--headless")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--verbose")
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disk-cache-size=150000000")
    driver = Chrome(options=options)
    return driver
