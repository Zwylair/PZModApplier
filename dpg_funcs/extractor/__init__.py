import shutil
import os.path
import logging
from dpg_funcs.extractor import seven_z, rar, zip
from dpg_funcs import classes
from dpg_funcs.funcs import *
from settings import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s (%(funcName)s)]: %(message)s')
logger.setLevel(logging.DEBUG)

extractors = {
    '.rar': rar.extractor,
    '.zip': zip.extractor,
    '.7z': seven_z.extractor
}


def get_clean_path_to_mod(dirty_mod_path: str) -> list[str]:
    """ This func unpacks mod path to clean dir that contains mod datas. (from "1234567890" to "1234567890/mods/new_mod") """

    out_mods_directories = []
    while True:
        dirty_mod_path: str
        all_files = os.listdir(dirty_mod_path)

        if 'media' in all_files and 'mod.info' in all_files:
            return out_mods_directories + [dirty_mod_path]
        else:
            dirty_mod_path = os.path.join(dirty_mod_path, all_files[0])


def scan_extracted_and_get_clean_paths(extracted_dir: str) -> list[str]:
    all_files = os.listdir(extracted_dir)

    # extracted dir = mod folder
    if 'media' in all_files and 'mod.info' in all_files:
        return [extracted_dir]

    all_mods_dirs = []
    for file in all_files:
        all_mods_dirs += get_clean_path_to_mod(os.path.join(extracted_dir, file))

    logger.debug(f'Got files: {all_files}, returned: {all_mods_dirs}')
    return all_mods_dirs


def extractor(filepath: str):
    if not os.path.exists(PROGRAM_MOD_DIR):
        os.mkdir(PROGRAM_MOD_DIR)
    os.makedirs(PZ_MODS_PATH, exist_ok=True)

    temp_dir = classes.TempDir()

    open_processing_window()
    logger.debug('Stage 1/2: Defining & Unpacking')

    for input_mod_object in os.listdir(filepath):
        input_mod_object = os.path.join(filepath, input_mod_object)
        mod_input_object_filename = os.path.split(input_mod_object)[-1]

        logger.debug('')
        logger.debug(f'Got packed mod: {input_mod_object}')
        dpg.set_value(
            'processing_text_item',
            '\n'.join(split_string_into_parts(f'Processing: {mod_input_object_filename}', 30))
        )

        # if mod object is folder:
        if os.path.isdir(input_mod_object):
            logger.debug('Packed mod is dir')

            shutil.copytree(input_mod_object, f'{temp_dir.path}/{mod_input_object_filename}')
            logger.debug('Copied to temp dir')
            continue

        # unpacking .zip, .rar, .7z
        for extension, callable_extractor in extractors.items():
            if input_mod_object.endswith(extension):
                logger.debug(f'Packed mod is archive')
                logger.debug(f'Using "{extension.lstrip(".")}" extractor')

                callable_extractor(temp_dir, input_mod_object)
                logger.debug('Extracted')

    logger.debug('')
    logger.debug('Stage 2/2: Moving unpacked mods')
    logger.debug('')

    # moving unpacked mods to pz dir
    for unpacked_mod in scan_extracted_and_get_clean_paths(temp_dir.path):
        mod_name = os.path.split(unpacked_mod)[-1]

        logger.debug(f'Moving mod: {mod_name}')

        try:
            shutil.move(unpacked_mod, os.path.join(PZ_MODS_PATH, mod_name))
        except Exception:
            pass  # already exists

    temp_dir.close()
    dpg.set_value('processing_text_item', 'Done')
    dpg.configure_item('done_window', no_title_bar=False, no_close=False)

    logger.debug('')
    logger.debug('Done')
