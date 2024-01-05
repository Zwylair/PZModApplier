import os
import rarfile

# paths
PZ_MODS_PATH = f'{os.getenv("userprofile")}\\Zomboid\\mods'
# PZ_MODS_PATH = f'{os.getcwd()}\\Zomboid\\mods'
PROGRAM_MOD_DIR = os.path.join(os.getcwd(), 'mods')
UNRAR_TOOL_PATH = os.path.join(os.getcwd(), 'bin\\unrar.exe')

# default values
MODS_FIELD_DEFAULT_VALUE = f'Add your mods by using Drag&Drop or moving them into "{PROGRAM_MOD_DIR}"'
MODS_FIELD_HEADER_DEFAULT_VALUE = 'Mods available to install'

#

rarfile.UNRAR_TOOL = UNRAR_TOOL_PATH
