import logging
import os
import dearpygui.dearpygui as dpg
from modules.o_funcs import apply_mods, update_mod_list_to_install
from modules.windows import mod_manager
from settings import PZ_MODS_PATH
from modules.logs_handler import LogsHandler

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(LogsHandler())

# create a main window
dpg.create_context()
dpg.create_viewport(title='Project Zomboid Mod Manager v1.0', small_icon='icon.ico', width=600, height=500, resizable=False)

with dpg.value_registry():
    dpg.add_string_value(tag='error_field_reg')

with dpg.window(width=9999, height=9999, no_title_bar=True, no_resize=True, no_close=True, no_move=True):
    with dpg.group(horizontal=True):
        dpg.add_button(label='Open Mods Folder', callback=lambda: os.startfile('mods'))
        dpg.add_button(label='Open Installed Mods Folder', callback=lambda: os.startfile(PZ_MODS_PATH))
        dpg.add_button(label='Apply mods', callback=apply_mods)

    dpg.add_separator()

    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text('Mods available to install:', tag='mod_list_2inst_text')
            dpg.add_button(label='Mod Manager', callback=mod_manager)
            dpg.add_button(label='Update', callback=update_mod_list_to_install)
        dpg.add_input_text(default_value="You haven't added any mods yet! By placing the mod\n"
                                         "archive in the 'mods' folder you can update this\n"
                                         "list!",
                           tag='mod_list_to_install', width=363, height=170, multiline=True, readonly=True)

    dpg.add_separator()

    with dpg.group():
        dpg.add_text('Logs:')
        dpg.add_input_text(tag='error_field', source='error_field_reg', width=dpg.get_viewport_width() - 31, multiline=True, readonly=True)

    update_mod_list_to_install()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
