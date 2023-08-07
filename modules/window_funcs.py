from os import listdir
from os.path import isdir
import dearpygui.dearpygui as dpg
from settings import PZ_MODS_PATH
from modules.get_mod_info import GetModInfo


class ModManagement:
    def __init__(self):
        self.mods = None
        self.enabled_mods_ids = None

        self.update_info()

    def update_info(self):
        with open(f'{PZ_MODS_PATH}/default.txt') as file:
            file_entry = file.read().split('\n')

            start_index, end_index = 0, 0
            for _ in file_entry:
                if _ == '{':
                    start_index = file_entry.index(_) + 1
                elif _ == '}':
                    end_index = file_entry.index(_)
                    break

            try:
                raw_mods = file_entry[start_index:end_index]
                raw_mods = [i[1:-1] for i in raw_mods]  # ['mod = modId', ...]
                enabled_mods_ids = [_.split(" = ")[1] for _ in raw_mods]
            except BaseException:
                enabled_mods_ids = []

        to_remove = ['examplemod']
        mods = [GetModInfo(f'{PZ_MODS_PATH}/{i}/mod.info') for i in listdir(PZ_MODS_PATH) if isdir(f'{PZ_MODS_PATH}/{i}') and i not in to_remove]

        self.mods = mods
        self.enabled_mods_ids = enabled_mods_ids

    def update_fields(self):
        self.mods: list[GetModInfo]
        out_mod_list = ''

        for mod in self.mods:
            name = f'{mod.name[:16]}...' if len(mod.name) > 16 else mod.name
            if mod.id in self.enabled_mods_ids:
                out_mod_list += f'* {name} [ID={mod.id}]\n'
            else:
                out_mod_list += f'{name} [ID={mod.id}]\n'

        if out_mod_list != '':
            dpg.set_value('mod_list_text', f'Mod-list ({len(self.mods)}):')
            dpg.set_value('mod_list', out_mod_list)
            dpg.configure_item('mod_list_combo', items=[i.id for i in self.mods])

        btn_text = '<- Disable This Mod' if dpg.get_value('mod_list_combo') in self.enabled_mods_ids else '<- Enable This Mod'
        dpg.set_item_label('enable_button', btn_text)

    def update_all(self):
        self.update_info()
        self.update_fields()

    def enable_or_disable_mod(self):
        mod_id: str = dpg.get_value('mod_list_combo')
        if mod_id != '':
            with open(f'{PZ_MODS_PATH}/default.txt', 'r') as file:
                file_entry = file.read().split('\n')

            if mod_id in self.enabled_mods_ids:  # Disable
                file_entry.remove(f'\tmod = {mod_id},')
            else:  # Enable
                for _ in file_entry:
                    if _ == '}':
                        file_entry.insert(file_entry.index(_), f'\tmod = {mod_id},')
                        break

            with open(f'{PZ_MODS_PATH}/default.txt', 'w') as file:
                file.write('\n'.join(file_entry))

            self.update_all()


def mods_combo_event(mod_manager: ModManagement, mod_id: str):
    btn_text = '<- Disable This Mod' if mod_id in mod_manager.enabled_mods_ids else '<- Enable This Mod'
    dpg.set_item_label('enable_button', btn_text)
