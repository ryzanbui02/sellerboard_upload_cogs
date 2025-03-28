import os
import tkinter as tk
import shutil
from datetime import datetime
from tkinter import filedialog

from typing import Dict, List


def get_folder_path() -> str:
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path


def get_files_to_upload_cogs(
    input_folder_path: str,
) -> Dict[str, List[Dict[str, str]]]:
    files: List[str] = os.listdir(input_folder_path)

    eu_files = []
    us_files = []

    for file_name in files:
        if file_name.endswith(".csv"):
            date_str = file_name[5:15]
            date_obj = datetime.strptime(date_str, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")
            file_obj = {
                "file_name": file_name,
                "file_path": os.path.join(input_folder_path, file_name),
                "batch_date": formatted_date,
            }
            if file_name.startswith("EU"):
                eu_files.append(file_obj)
            elif file_name.startswith("US"):
                us_files.append(file_obj)
    return {
        "eu_files": eu_files,
        "us_files": us_files,
    }


def move_file(file_path: str, target_folder: str) -> None:
    if os.path.isfile(file_path) and file_path.endswith(".csv"):
        new_file_path = os.path.join(
            target_folder, os.path.basename(file_path)
        )
        shutil.move(file_path, new_file_path)
