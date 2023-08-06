import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.ext.proxy import *

else:
    from .._api.ext.proxy import *

