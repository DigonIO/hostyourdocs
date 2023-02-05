from flet import Event, Page, Text, TextButton, icons
from hyd_client import ApiClient

from hyd.frontend.view.util import ViewManager, ViewType

####################################################################################################
### Landing View
####################################################################################################


def show_landing_view(*, page: Page, api_client: ApiClient) -> None:
    def on_login_button_click(event: Event) -> None:
        ViewManager.show(ViewType.LOGIN)

    page.appbar.title = Text("HostYourDocs")
    page.appbar.actions = [TextButton("Login", icon=icons.LOGIN, on_click=on_login_button_click)]
    page.clean()
    page.update()
