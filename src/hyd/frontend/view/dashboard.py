from flet import Page, Text
from hyd_client import ApiClient

####################################################################################################
### Dashboard View
####################################################################################################


def show_dashboard_view(*, page: Page, api_client: ApiClient) -> None:
    page.appbar.title = Text("HostYourDocs - Dashboard")
    page.clean()

    page.add(
        Text("Hello admin", size=30),
        Text("TODO", size=30),
    )

    page.update()
