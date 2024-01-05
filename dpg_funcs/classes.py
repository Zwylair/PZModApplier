import string
import random
import shutil
import os.path


class TempDir:
    def __init__(self):
        while True:
            self.name = 'tmp0' + ''.join([random.choice(string.ascii_lowercase) for _ in range(9)])
            self.path = os.path.join(os.getenv('tmp'), self.name)

            if not os.path.exists(self.path):
                os.mkdir(self.path)
                break

    def close(self):
        shutil.rmtree(self.path)


# class Mod:
#     def __init__(self, path: str):
#         with open(os.path.join(path, 'mod.info')) as mod_info_file:
#             content = mod_info_file.readlines()
#             content = {i[0]: '='.join(i[1:]) for i in content if i}
#
#         self.name = content.get('name')
#         self.id = content.get('id')
#         self.description = content.get('description')
#         self.pack = content.get('pack')
#         self.tiledef = content.get('tiledef')
#         self.icon = content.get('icon')
#         self.minimal_pz_version = content.get('versionMin')
#         self.mod_version = content.get('modVersion')
#         self.url = content.get('url')
#         self.posters = content.get('poster')
#         self.authors = content.get('authors')
#         self.tags = content.get('tags')
#
#         if self.posters:
#             self.posters = self.posters.split(',')
#
#         if self.authors:
#             self.authors = self.authors.split(',')
#
#         if self.tags:
#             self.tags = self.tags.split(',')
