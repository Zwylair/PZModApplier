import py7zr
from dpg_funcs import classes


def extractor(temp_dir: classes.TempDir, filepath: str):
    archive = py7zr.SevenZipFile(filepath)
    archive.extractall(f'{temp_dir.path}/')
