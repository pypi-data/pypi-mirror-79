import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.data import *

else:
    from ._api.data import *
