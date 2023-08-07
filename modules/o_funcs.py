import logging
import random
import string
from pathlib import Path
import os.path
import shutil
from py7zr import SevenZipFile
from zipfile import ZipFile
from rarfile import RarFile
import dearpygui.dearpygui as dpg
from settings import PZ_MODS_PATH
from modules.windows import display_done_window

logger = logging.getLogger('logger.o_funcs')
logger.setLevel(logging.DEBUG)


def gen_rand_str(length: int = 12) -> str:
    return ''.join([random.choice(string.ascii_lowercase) if random.randint(0, 1) else random.choice(string.digits) for _ in range(length)])


def extract_mods():
    temp_dir = f'{os.getenv("tmp")}/{gen_rand_str()}'
    os.mkdir(temp_dir)

    for mod in os.listdir('mods'):
        try:
            if mod.endswith('.7z'):
                SevenZipFile(f'mods/{mod}').extractall(f'{temp_dir}/')
            elif mod.endswith('.zip'):
                ZipFile(f'mods/{mod}').extractall(f'{temp_dir}/')
            elif mod.endswith('.rar'):
                RarFile(f'mods/{mod}').extractall(f'{temp_dir}/')
            else:
                logging.error(f'{mod[:9]}... is not a valid mod-file')
        except BaseException as err:
            logging.error(err)
        else:
            mod_dir = None

            while True:
                check_dirs = []
                for root, dirs, files in os.walk(f'{temp_dir}/'):
                    for name in dirs:
                        check_dirs.append(os.path.join(root, name))

                for directory in check_dirs:
                    listdir = os.listdir(directory)
                    if 'media' in listdir and 'mod.info' in listdir:
                        mod_dir = directory
                        break
                
                if mod_dir is None:
                    logger.info(f'{mod} is not a mod. Skipping')
                    break

                try:
                    logger.debug(f'Mod dir: {mod_dir} ; Destination: {PZ_MODS_PATH}/{os.path.split(mod_dir)[1]} ; Mod: {mod}')
                    shutil.move(mod_dir, f'{PZ_MODS_PATH}/{os.path.split(mod_dir)[1]}')
                except BaseException as err:
                    if 'already exists' not in str(err):
                        logging.error(err)
                break

    shutil.rmtree(f'{temp_dir}/')


def apply_mods():
    extract_mods()
    display_done_window()


def update_mod_list_to_install():
    mods = [Path(i).stem for i in os.listdir('mods')]
    if mods:
        dpg.set_value('mod_list_to_install', '\n'.join(mods))
        dpg.set_value('mod_list_2inst_text', f'Mods available ({len(mods)}):')
