import time
# import json
# import pickle
# import base64
import os.path
import threading
from send2trash import send2trash
from dpg_funcs.classes import *
from dpg_funcs.extractor import *
from dpg_funcs.funcs import *
from settings import *


# def dump_mods(mod_array: list[classes.Mod]):
#     coded = list(map(lambda item: pickle.dumps(item), mod_array))
#     coded = list(map(lambda item: base64.b64encode(item).decode(), coded))
#     coded = json.dumps(coded)
#
#     dpg.set_value('mods_objects_storage', coded)
#
#
# def load_mods() -> list[classes.Mod]:
#     decoded = dpg.get_value('mods_objects_storage')
#     decoded = list(map(lambda item: base64.b64decode(item), decoded))
#     decoded = list(map(lambda item: pickle.loads(item), decoded))
#
#     return decoded


logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.DEBUG)


def update_mod_list():
    mods = os.listdir('mods')

    mods_field_value = '\n'.join(mods) if mods else MODS_FIELD_DEFAULT_VALUE
    mods_field_header_value = f'{MODS_FIELD_HEADER_DEFAULT_VALUE} ({len(mods)}):' if mods else f'{MODS_FIELD_HEADER_DEFAULT_VALUE}:'

    dpg.set_value('mods_field_value', mods_field_value.format())
    dpg.set_value('mods_field_header_value', mods_field_header_value)


def clear_program_mod_dir():
    for file in os.listdir(PROGRAM_MOD_DIR):
        filepath = os.path.join(PROGRAM_MOD_DIR, file)

        send2trash(filepath)
        logger.debug(f'Sent to trash: {filepath}')


def drop_handler(filepaths: list[str]):
    for filepath in filepaths:
        filename = os.path.split(filepath)[-1]

        if os.path.isdir(filepath):
            shutil.copytree(filepath, f'mods/{filename}')
        else:
            shutil.copy(filepath, f'mods/{filename}')


def start_delayed_mod_updater():
    def delayed_mod_list_update():
        while True:
            update_mod_list()
            time.sleep(1)

    thread = threading.Thread(target=delayed_mod_list_update)
    thread.daemon = True
    thread.start()
