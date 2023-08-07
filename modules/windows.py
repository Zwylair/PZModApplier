import dearpygui.dearpygui as dpg


def display_done_window():
    with dpg.window(width=200, height=100, pos=[92, 73.5], no_resize=True):
        dpg.add_text('Done!\n'
                     'Dont forget to remove your\n'
                     'old mods in "mods" folder)')


def mod_manager():
    from modules.window_funcs import ModManagement, mods_combo_event

    manager = ModManagement()

    with dpg.window(width=384, height=311, no_resize=True, tag='mod_manager_window'):
        with dpg.group(horizontal=True):
            dpg.add_combo(tag='mod_list_combo', width=200, callback=lambda tag, item: mods_combo_event(manager, item))
            dpg.add_button(label='<- Enable This Mod', tag='enable_button', callback=lambda: manager.enable_or_disable_mod())

        with dpg.group(horizontal=True):
            dpg.add_text('Mod-list:', tag='mod_list_text')
            dpg.add_text('("*" means that the mod is on)')
            dpg.add_button(label='Update', callback=lambda: manager.update_all())
        dpg.add_input_text(default_value='There are no mods(', tag='mod_list', width=366, height=199, multiline=True, readonly=True)

        manager.update_info()
        manager.update_fields()
