import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.database import *

else:
    from .._api.database import *

