"""
Model classes for the Humble Bundle API

This module only is guaranteed to only contain model class definitions
"""

__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

class BaseModel(object):
    def __init__(self, client, data):
        self._client = client

    def __str__(self):
        return str({key: self.__dict__[key] for key in self.__dict__ if key != '_client'})

    def __repr__(self):
        return repr(self.__dict__)

    def __iter__(self):
        return self.__dict__.__iter__()

class Order(BaseModel):
    def __init__(self, client, data):
        super(Order, self).__init__(client, data)
        self.product = Product(client, data['product'])
        self.subscriptions = [Subscription(client, sub) for sub in data['subscriptions']]
        self.thankname = data['thankname']
        self.claimed = data['claimed']
        self.gamekey = data['gamekey']
        self.country = data['country']
        self.giftee = data['giftee']
        self.leaderboard = data['leaderboard']
        self.owner_username = data['owner_username']
        self.platforms = [plat for plat, v in data['platform'].items() if v > 0]
        self.subproducts = [Subproduct(client, prod) for prod in data.get('subproducts', [])]

    def __repr__(self):
        return "Order: <%s>" % self.product.machine_name

    def ensure_subproducts(self, *args, **kwargs):
        if not hasattr(self, 'subproducts'):
            self.__dict__.update(self._client.order(self.gamekey, *args, **kwargs).__dict__)
        return self


class Product(BaseModel):
    def __init__(self, client, data):
        super(Product, self).__init__(client, data)
        self.category = data['category']
        self.human_name = data['human_name']
        self.machine_name = data['machine_name']
        self.supports_canonical = data['supports_canonical']

    def __repr__(self):
        return "Product: <%s>" % self.machine_name


class Subscription(BaseModel):
    def __init__(self, client, data):
        super(Subscription, self).__init__(client, data)
        self.human_name = data['human_name']
        self.list_name = data['list_name']
        self.subscribed = data['subscribed']

    def __repr__(self):
        return "Subscription: <%s : %s>" % (self.list_name, self.subscribed)


class Subproduct(BaseModel):
    def __init__(self, client, data):
        super(Subproduct, self).__init__(client, data)
        self.tpkd_machine_names = [name for name in data['tpkd_machine_names']]
        self.preorder = data['preorder']
        self.machine_name = data['machine_name']
        self.parent = data['parent']
        self.payee = Payee(client, data['payee'])
        self.url = data['url']
        self.downloads = [Download(client, download) for download in data['downloads']]
        self.visible = data['visible']
        self.meta_data = data['meta_data']
        self.human_name = data['human_name']
        self.custom_download_page_box_html = data['custom_download_page_box_html']
        self.icon = data['icon']

    def __repr__(self):
        return "Subproduct: <%s>" % self.machine_name


class Payee(BaseModel):
    def __init__(self, client, data):
        super(Payee, self).__init__(client, data)
        self.human_name = data['human_name']
        self.machine_name = data['machine_name']

    def __repr__(self):
        return "Payee: <%s>" % self.machine_name


class Download(BaseModel):
    def __init__(self, client, data):
        super(Download, self).__init__(client, data)
        self.machine_name = data['machine_name']
        self.parent = data['parent']
        self.platform = data['platform']
        self.download_struct = [DownloadStruct(client, struct) for struct in data['download_struct']]
        self.options_dict = data['options_dict']
        self.download_identifier = data['download_identifier']
        self.download_version_number = data['download_version_number']

    def sign_download_url(self, *args, **kwargs):
        return self._client.sign_download_url(self.machine_name, *args, **kwargs)

    def __repr__(self):
        return "Download: <%s>" % self.machine_name


class DownloadStruct(BaseModel):
    def __init__(self, client, data):
        super(DownloadStruct, self).__init__(client, data)
        self.sha1 = data.get('sha1', None)
        self.name = data.get('name', None)
        self.message = data.get('message', None)
        self.url = Url(client, data.get('url', {}))
        self.external_link = data.get('external_link', None)
        self.recommend_bittorrent = data['recommend_bittorrent']
        self.human_size = data['human_size']
        self.file_size = data.get('file_size', None)
        self.md5 = data.get('md5', None)
        self.fat32_warning = data['fat32_warning']
        self.size = data.get('size', None)
        self.small = data.get('small', None)


class Url(BaseModel):
    def __init__(self, client, data):
        super(Url, self).__init__(client, data)
        self.web = data.get('web', None)
        self.bittorrent = data.get('bittorrent', None)