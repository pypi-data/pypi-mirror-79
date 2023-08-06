import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.store import *

else:
    from ._api.store import *
