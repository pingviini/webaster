from persistent.mapping import PersistentMapping
from persistent import Persistent
from repoze.folder import Folder


class Webaster(PersistentMapping):
    __parent__ = __name__ = None


class Buildouts(Folder):
    pass


class Buildout(Folder):
    def __init__(self, name, base, description):
        super(Buildout, self).__init__()
        self.name = name
        self.base = base
        self.description = description


class File(Persistent):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Template(File):
    def __init__(self, name, data):
        self.__name__ = name
        self.data = data


class BaseBuildouts(Folder):
    pass


class BaseBuildout(Folder):
    def __init__(self, title, version, url):
        super(BaseBuildout, self).__init__()
        self.title = title
        self.version = version
        self.url = url


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Webaster()
        zodb_root['app_root'] = app_root
        app_root[u'buildouts'] = Buildouts()
        app_root[u'buildouts'].__parent__ = app_root
        app_root[u'base_buildouts'] = BaseBuildouts()
        app_root[u'base_buildouts'].__parent__ = app_root

        import transaction
        transaction.commit()
    return zodb_root['app_root']
