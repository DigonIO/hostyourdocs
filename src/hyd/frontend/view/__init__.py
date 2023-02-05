from flet import Page
from hyd_client import ApiClient
from hyd_client.api.user_api import UserApi
from hyd_client.exceptions import ApiException, UnauthorizedException

from hyd.frontend.security import decrypt_client_storage_value
from hyd.frontend.storage_key import ClientStorageKey as CSK
from hyd.frontend.storage_key import SessionStorageKey as SSK
from hyd.frontend.view.access_token_list import show_access_token_list_view
from hyd.frontend.view.dashboard import show_dashboard_view
from hyd.frontend.view.landing import show_landing_view
from hyd.frontend.view.login import show_login_view
from hyd.frontend.view.project_list import show_project_list_view
from hyd.frontend.view.util import ViewManager, ViewType, build_appbar_actions

ViewManager._view_type_mapping = {
    ViewType.LANDING: show_landing_view,
    ViewType.LOGIN: show_login_view,
    ViewType.DASHBOARD: show_dashboard_view,
    ViewType.PROJECT_LIST: show_project_list_view,
    ViewType.ACCESS_TOKEN_LIST: show_access_token_list_view,
}

####################################################################################################
### Init View
####################################################################################################


def init_view(*, page: Page, api_client: ApiClient) -> None:
    ViewManager._page = page
    ViewManager._api_client = api_client

    encrypted_token = page.client_storage.get(CSK.AUTH_TOKEN)
    if encrypted_token is None:
        return ViewManager.show(ViewType.LANDING)

    access_token: str = decrypt_client_storage_value(encrypted_value=encrypted_token)
    api_client.configuration.access_token = access_token

    user_api = UserApi(api_client=api_client)
    try:
        user_api.api_v1_user_greet_get_with_http_info()
    except (UnauthorizedException, ApiException):
        api_client.configuration.access_token = None
        ViewManager.show(ViewType.LANDING)
    else:
        page.session.set(SSK.USERNAME, "admin")  # TODO request user meta data

        build_appbar_actions(page=page, api_client=api_client)
        ViewManager.show(ViewType.DASHBOARD)
