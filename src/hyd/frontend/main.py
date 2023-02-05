from flet import (
    AppBar,
    CircleAvatar,
    Container,
    ElevatedButton,
    Icon,
    Page,
    Text,
    TextButton,
    TextField,
    View,
    app,
    colors,
    icons,
    padding,
    theme,
)
from hyd_client import ApiClient, Configuration

from hyd.frontend.views import init_view

PROTOCOL = "http"
BACKEND_ADDRESS = "127.0.0.1"
BACKEND_PORT = "8000"

BACKEND_URL = PROTOCOL + "://" + BACKEND_ADDRESS + ":" + BACKEND_PORT

####################################################################################################
### Main
####################################################################################################


def main(page: Page) -> None:
    configuration = Configuration(host=BACKEND_URL)
    api_client = ApiClient(configuration=configuration)

    _setup_page(page=page)

    init_view(page=page, api_client=api_client)


####################################################################################################
### Util
####################################################################################################


def _setup_page(page: Page) -> None:
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    page.window_resizable = True
    page.title = "HostYourDocs"
    page.theme = theme.Theme(color_scheme_seed="blue")
    page.window_height = page.window_height - 100
    page.window_width = page.window_width - 200
    page.appbar = AppBar(bgcolor=colors.SURFACE_VARIANT)
