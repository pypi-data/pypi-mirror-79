import os

name = "dcms"

if os.environ.get('IN_CRAWL_PROCESS'):
    from api import *

else:
    from ._api import *
