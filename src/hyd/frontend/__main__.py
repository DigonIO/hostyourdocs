from flet import WEB_BROWSER, app

from hyd.frontend.const import PORT
from hyd.frontend.main import main

app(target=main, view=WEB_BROWSER, port=PORT)
