import rarfile
from dpg_funcs import classes


def extractor(temp_dir: classes.TempDir, filepath: str):
    archive = rarfile.RarFile(filepath)
    archive.extractall(f'{temp_dir.path}/')
