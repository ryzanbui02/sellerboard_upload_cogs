from selenium.webdriver import Chrome, Remote
from selenium.webdriver.common.by import By
from typing import Union
from .client_page import ClientPage

PRODUCT_PAGE_ELEMENT = "//a[@href='/en/products']"
IMPORT_ELEMENT = "//a[@data-type='products' and @data-toggle='modal' and @data-target='#importExport']"
EXPORT_ELEMENT = "//a[@data-target='#exportModal']"
SEND_TO_MAIL_ELEMENT = "//button[@ng-click='sendToEmail($event)']"
DROPDOWN_ELEMENT = "field_accountingMethod"

UPDATE_METHOD = "Weighted"
BY_BATCH_OPTION = "//li[@ng-repeat='(key, data) in importTabsData' and contains(., 'By batch')]"
FILE_INPUT = "//input[@type='file']"
DATE_INPUT = "field_batchDate"
IMPORT_BUTTON = "button.btn.btn-primary[ng-click='startImport()']"
IMPORT_SUCCESS_BUTTON = "div.title[ng-show='importSuccess']"


class InventoryPage(ClientPage):
    def __init__(self, chrome_driver: Union[Chrome, Remote]):
        super().__init__(chrome_driver)

    def __str__(self) -> str:
        return "InventoryPage"

    def access_inventory(self) -> None:
        self.click_button(strategy=By.XPATH, target=PRODUCT_PAGE_ELEMENT)

    def get_inventory(self) -> None:
        self.access_inventory()
        self.click_button(strategy=By.XPATH, target=EXPORT_ELEMENT)
        self.force_click_button(strategy=By.XPATH, target=SEND_TO_MAIL_ELEMENT)
        # self.refresh_page()

    def upload_cogs_by_batch(
        self, input_file_path: str, batch_date: str
    ) -> None:
        self.access_inventory()
        self.click_button(By.XPATH, IMPORT_ELEMENT)
        self.click_button(By.XPATH, BY_BATCH_OPTION)
        self.send_keys(By.XPATH, FILE_INPUT, input_file_path)
        self.click_button(By.CSS_SELECTOR, IMPORT_BUTTON)
        self.select_from_dropdown(By.NAME, DROPDOWN_ELEMENT, UPDATE_METHOD)
        self.send_keys(By.NAME, DATE_INPUT, batch_date)
        self.click_button(By.CSS_SELECTOR, IMPORT_BUTTON)
        self.wait_for_elm(By.CSS_SELECTOR, IMPORT_SUCCESS_BUTTON, 3600)
        # self.refresh_page()
