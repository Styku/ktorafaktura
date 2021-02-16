import pdfplumber
import subprocess
from pathlib import Path
from config import Config
from shutil import move

def scan(path):
    args = [Config.get('naps2_path'), '-o', path]
    subprocess.run(args) 

def read_txt(path) -> str:
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    return text

def read_any(path) -> str:
    text = read_txt(path)
    if not text:
        new_path = run_ocr(path)
        if new_path:
            text = read_txt(new_path)
        else: 
            return None
    return text

def run_ocr(path, overwrite=True) -> str:
    path_obj = Path(path)
    new_path = path_obj.parent / '{}_ocr{}'.format(path_obj.stem, path_obj.suffix)
    if new_path.is_file():
        return new_path
    args = ['ocrmypdf', path_obj, new_path]
    subprocess.run(args)
    if overwrite:
        move(new_path, path_obj)
        new_path = path_obj
    return new_path
