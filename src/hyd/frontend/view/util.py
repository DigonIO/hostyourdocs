from enum import Enum, auto
from typing import Callable

from flet import Event, Page, PopupMenuButton, PopupMenuItem, icons
from hyd_client import ApiClient

####################################################################################################
### ViewManager
####################################################################################################


class ViewType(Enum):
    LANDING = auto()
    LOGIN = auto()
    DASHBOARD = auto()
    PROJECT_LIST = auto()
    ACCESS_TOKEN_LIST = auto()


class ViewManager:
    _view_type_mapping: dict[ViewType, Callable[[Page, ApiClient], None]]
    _page: Page
    _api_client: ApiClient

    @classmethod
    def show(cls, view_type: ViewType) -> None:
        cls._view_type_mapping[view_type](page=cls._page, api_client=cls._api_client)


####################################################################################################
### AppBar
####################################################################################################


def build_appbar_actions(*, page: Page, api_client: ApiClient) -> None:
    def on_dashboard_button_click(event: Event) -> None:
        ViewManager.show(ViewType.DASHBOARD)

    def on_projects_button_click(event: Event) -> None:
        ViewManager.show(ViewType.PROJECT_LIST)

    def on_access_tokens_button_click(event: Event) -> None:
        ViewManager.show(ViewType.ACCESS_TOKEN_LIST)

    def on_logout_button_click(event: Event) -> None:
        ViewManager.show(ViewType.LANDING)

    page.appbar.actions = [
        PopupMenuButton(
            icon=icons.MENU,
            items=[
                PopupMenuItem(
                    text="Dashboard", icon=icons.PERSON, on_click=on_dashboard_button_click
                ),
                PopupMenuItem(),  # divider
                PopupMenuItem(
                    text="Projects", icon=icons.FOLDER, on_click=on_projects_button_click
                ),
                PopupMenuItem(
                    text="Access Tokens", icon=icons.KEY, on_click=on_access_tokens_button_click
                ),
                PopupMenuItem(),  # divider
                PopupMenuItem(text="Logout", icon=icons.LOGOUT, on_click=on_logout_button_click),
            ],
        ),
    ]
