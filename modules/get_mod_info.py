from typing import Union


class GetModInfo:
    def __init__(self, mod_info_filepath: str):
        self.mod_info_fp = mod_info_filepath

        with open(self.mod_info_fp, 'rb') as mod_info_obj:
            mod_info = [i for i in mod_info_obj.read().split(b'\n') if i != '']

            new_minfo = {}
            posters = []
            for i in mod_info:
                if i != '':
                    index = mod_info.index(i)
                    items = i.split(b'=')  # ['id', 'my_mod'] or ['name', 'My mod!']

                    if mod_info[index].startswith(b'poster'):
                        posters.append('='.join([i.decode() for i in items[1:]]).replace('\r', ''))
                    else:
                        new_minfo |= {items[0].decode(): '='.join([i.decode() for i in items[1:]]).replace('\r', '')}

            new_minfo |= {'poster': posters}

        self.name: Union[None, str] = new_minfo.get('name')
        self.id: Union[None, str] = new_minfo.get('id')
        self.description: Union[None, str] = new_minfo.get('description')
        self.pack: Union[None, str] = new_minfo.get('pack')
        self.tiledef: Union[None, str] = new_minfo.get('tiledef')
        self.icon: Union[None, str] = new_minfo.get('icon')
        self.version_min: Union[None, str] = new_minfo.get('versionMin')
        self.mod_version: Union[None, str] = new_minfo.get('modVersion')
        self.url: Union[None, str] = new_minfo.get('url')
        self.posters: Union[None, list] = new_minfo.get('poster')
        self.authors: Union[None, list] = None if new_minfo.get('tags') is None else new_minfo.get('authors').split(',')
        self.tags: Union[None, list] = None if new_minfo.get('tags') is None else new_minfo.get('tags').split(',')
