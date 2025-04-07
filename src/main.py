import os
import json
import logging
import time

from dotenv import load_dotenv

load_dotenv()

from logging.config import dictConfig
from typing import Dict, List

from common import get_chrome_driver
from common.helpers import get_folder_path, get_files_to_upload_cogs, move_file
from sellerboard import InventoryPage

os.system("cls")

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)

with open(os.path.join(ROOT_DIR, "configs", "logging_cfg.json")) as lf:
    dictConfig(json.load(lf))
logger = logging.getLogger("default")

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SLEEP_TIME = 30


def upload_one(cli: InventoryPage, file: Dict[str, str]) -> None:
    file_path = file["file_path"]
    batch_date = file["batch_date"]
    cli.upload_cogs_by_batch(file_path, batch_date)


def upload_all(
    cli: InventoryPage,
    files: Dict[str, List[Dict[str, str]]],
    uploaded_folder: str,
    error_folder: str,
) -> None:
    def process_file(file: Dict[str, str]) -> None:
        file_path = file.get("file_path")
        file_name = file.get("file_name")
        try:
            logger.info(f"Uploading: {file_name}")
            upload_one(cli, file)
            move_file(file_path, uploaded_folder)
            logger.info(f"Uploaded: {file_name}")
        except KeyboardInterrupt:
            logger.warning("Interrupted by user")
        except Exception as e:
            logger.error(f"Failed to upload: {file_name}")
            logger.error(e)
            move_file(file_path, error_folder)
            time.sleep(600)
        finally:
            cli.refresh_page()
            time.sleep(SLEEP_TIME)

    eu_files = files["eu_files"]
    us_files = files["us_files"]
    for file in eu_files:
        process_file(file)

    cli.switch_marketplace()
    time.sleep(SLEEP_TIME)

    for file in us_files:
        process_file(file)


def upload_report(cli: InventoryPage, input_folder: str) -> None:
    uploaded_folder = os.path.join(os.path.dirname(input_folder), "uploaded")
    error_folder = os.path.join(os.path.dirname(input_folder), "error")
    os.makedirs(uploaded_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)
    files = get_files_to_upload_cogs(input_folder)
    upload_all(cli, files, uploaded_folder, error_folder)


def main():
    input_folder = get_folder_path()
    if input_folder is None:
        return

    driver = get_chrome_driver()
    cli = InventoryPage(driver)
    try:
        cli.login(EMAIL, PASSWORD)
        upload_report(cli, input_folder)
        logger.info("All files are uploaded to Sellerboard")
    except:
        logger.error("Error happened")
    finally:
        cli.quit_driver()


if __name__ == "__main__":
    main()
