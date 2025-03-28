from .base_page import BasePage
from selenium.webdriver import Chrome, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Union

LOGIN_URL = "https://app.sellerboard.com/en/auth/login/"
LOGOUT_ELEMENT = "//li[contains(@class, 'logout')]//a"


class Marketplace:
    US: str = "US"
    EU: str = "EU"


class ClientPage(BasePage):
    def __init__(self, driver: Union[Chrome, Remote]) -> None:
        super().__init__(driver)

    def __str__(self) -> str:
        return "ClientPage"

    def login(self, email: str, password: str) -> None:
        self.get(LOGIN_URL)
        self.send_keys(strategy=By.ID, target="username", keys_to_send=email)
        self.send_keys(
            strategy=By.ID,
            target="password",
            keys_to_send=password + Keys.ENTER,
        )

    def logout(self) -> None:
        self.select_account()
        self.click_button(strategy=By.XPATH, target=LOGOUT_ELEMENT)

    def select_account(self) -> None:
        self.click_button(
            strategy=By.CLASS_NAME, target="accountFilter-selected"
        )

    def switch_marketplace(self, marketplace: str = "US") -> None:
        self.select_account()
        text = "USA" if marketplace == Marketplace.US else "eve.n@zendom.co.uk"
        target = f"//a[contains(@class, 'accountFilter-dropdown-list-item-link')]//span[contains(text(), '{text}')]"
        self.click_button(strategy=By.XPATH, target=target)
