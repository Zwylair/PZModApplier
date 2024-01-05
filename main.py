import os.path
import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
import dnd_setup
import dpg_funcs
from settings import *


if not os.path.exists(PROGRAM_MOD_DIR):
    os.mkdir(PROGRAM_MOD_DIR)
os.makedirs(PZ_MODS_PATH, exist_ok=True)

dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='PZ Mod Applier v2.0', small_icon='bin/icon.ico', width=600, height=500, resizable=False)

#

with dpg.font_registry():
    with dpg.font('bin/ubuntu_regular.ttf', 14, default_font=True, id='ubuntu'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)

    with dpg.font('bin/ubuntu_regular.ttf', 20, default_font=False, id='ubuntu_bigger'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
dpg.bind_font('ubuntu')

#

with dpg.value_registry():
    dpg.add_string_value(tag='mods_field_value')
    dpg.add_string_value(tag='mods_field_header_value', default_value=MODS_FIELD_HEADER_DEFAULT_VALUE)
    # dpg.add_string_value(tag='mods_objects_storage')

#

with dpg.window(width=600, height=500, no_title_bar=True, no_resize=True, no_close=True, no_move=True) as window:
    hint_text = '\n'.join(dpg_funcs.split_string_into_parts(MODS_FIELD_DEFAULT_VALUE, 64))
    hint_text_obj = dpg.add_text(hint_text, color=(168, 216, 167),)
    dpg.bind_item_font(hint_text_obj, 'ubuntu_bigger')

    dpg.add_spacer(height=6)

    dpg.add_text(source='mods_field_header_value')
    dpg.add_input_text(multiline=True, readonly=True, width=dpg.get_viewport_width() - 31, height=270)

    dpg.add_separator()
    dpg.add_spacer()

    with dpg.group(horizontal=True):
        dpg.add_button(label=f'Open "{PROGRAM_MOD_DIR}"', callback=lambda: os.startfile(PROGRAM_MOD_DIR))
        dpg.add_button(label=f'Open "{PZ_MODS_PATH}"', callback=lambda: os.startfile(PZ_MODS_PATH))

    dpg.add_spacer(height=8)

    with dpg.group(horizontal=True):
        dpg.add_button(label='Apply mods', callback=lambda: dpg_funcs.extractor(PROGRAM_MOD_DIR))
        dpg.add_button(label=f'Move to bin mods in "{PROGRAM_MOD_DIR}"', callback=dpg_funcs.clear_program_mod_dir)

    dpg_funcs.start_delayed_mod_updater()

#

dpg.set_primary_window(window, True)
dnd_setup.setup(dpg_funcs.drop_handler)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
