import os
import shutil
import cx_Freeze
import py7zr
import settings

executables = [
    cx_Freeze.Executable(
        script='main.py',
        base='Win32GUI' if settings.IS_GUI else None,
        icon=settings.ICON_PATH
    )
]

build_options = {
    'packages': ['dearpygui', 'py7zr', 'rarfile'],
    'excludes': [],
    'include_files': ['modules', 'icon.ico', 'settings.py', 'unrar.exe'],
}

# Создание exe-файла
cx_Freeze.setup(
    name='PZModApplier',
    version='1.0',
    options={'build_exe': build_options},
    executables=executables,
)

directory = f'build/{os.listdir("build")[0]}'
file_list = []

print()
print(f'packing all to {settings.BUILT_ARCHIVE_NAME}')
print()

with py7zr.SevenZipFile(settings.BUILT_ARCHIVE_NAME, mode='w') as built:
    for root, dirs, files in os.walk(directory):
        for file in files:
            orig_dir, arc_dir = f'{root}/{file}', f'{root.replace("build/", "")}/{file}'
            print(f'packing {orig_dir} -> {arc_dir}')

            built.write(orig_dir, arc_dir)
        for subdir in dirs:
            orig_dir, arc_dir = f'{root}/{subdir}', f'{root.replace("build/", "")}/{subdir}'
            print(f'packing {orig_dir} -> {arc_dir}')

            built.write(orig_dir, arc_dir)

print()
print('packing done')
print('deleting build dir')

shutil.rmtree('build')

print('done')
