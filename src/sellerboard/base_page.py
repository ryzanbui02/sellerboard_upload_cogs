import selenium.common.exceptions as se
from selenium.webdriver import Chrome, Remote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from typing import Any, Callable, Union


class BasePage:
    driver: Union[Chrome, Remote]

    def __init__(self, driver: Union[Chrome, Remote]) -> None:
        self.driver = driver

    def __str__(self) -> str:
        return "BasePage"

    def get(self, url: str) -> None:
        self.driver.get(url)

    def refresh_page(self) -> None:
        self.driver.refresh()

    def quit_driver(self) -> None:
        self.driver.quit()

    def wait(self, timeout: int = 10) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)

    @staticmethod
    def handle_error(func: Callable[[], Any], **kwargs: dict[str, Any]) -> Any:
        target = kwargs.get("target")
        try:
            return func()
        except se.TimeoutException:
            raise TimeoutError(f"Timeout error: {target}")
        except se.NoSuchElementException:
            raise Exception(f"Element not found: {target}")
        except se.ElementNotInteractableException:
            raise Exception(f"Element not interactable: {target}")
        except Exception:
            raise Exception(f"Something went wrong: {target}")

    def wait_for_elm(
        self, strategy: str, target: str, timeout: int = 10
    ) -> WebDriverWait:
        def func():
            elm = self.wait(timeout).until(
                EC.visibility_of_element_located((strategy, target))
            )
            return elm

        return self.handle_error(func, target=target)

    def send_keys(
        self, strategy: str, target: str, keys_to_send: str, timeout: int = 10
    ) -> None:
        if not strategy or not target or not keys_to_send:
            raise AttributeError("Please send valid parameters")

        def func():
            input_elm = self.wait(timeout).until(
                EC.presence_of_element_located((strategy, target))
            )
            try:
                input_elm.clear()
            except se.ElementNotInteractableException:
                pass
                # print(f"Cannot clear input element {target}")
            input_elm.send_keys(keys_to_send)

        return self.handle_error(func, target=target)

    def click_button(
        self, strategy: str, target: str, timeout: int = 10
    ) -> None:
        def func():
            button = self.wait(timeout).until(
                EC.element_to_be_clickable((strategy, target))
            )
            button.click()

        return self.handle_error(func, target=target)

    def force_click_button(self, strategy: str, target: str, timeout=10):
        def func():
            button = self.wait(timeout).until(
                EC.presence_of_element_located((strategy, target))
            )
            self.driver.execute_script("arguments[0].click();", button)

        return self.handle_error(func, target=target)

    def select_from_dropdown(
        self, strategy: str, dropdown_elm: str, target: str, timeout: int = 10
    ) -> None:
        """
        Click on an element in a dropdown.
        """

        def func():
            dropdown = self.wait(timeout).until(
                EC.presence_of_element_located((strategy, dropdown_elm))
            )
            select = Select(dropdown)
            select.select_by_visible_text(target)

        return self.handle_error(func, target=target)
