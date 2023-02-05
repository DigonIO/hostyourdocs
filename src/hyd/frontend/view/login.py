from flet import (
    AlertDialog,
    ElevatedButton,
    Event,
    Page,
    Text,
    TextButton,
    TextField,
    icons,
)
from hyd_client import ApiClient
from hyd_client.api.user_api import UserApi
from hyd_client.exceptions import ApiException, UnauthorizedException
from hyd_client.models.token_schema import TokenSchema

from hyd.frontend.security import encrypt_client_storage_value
from hyd.frontend.storage_key import ClientStorageKey as CSK
from hyd.frontend.storage_key import SessionStorageKey as SSK
from hyd.frontend.view.util import ViewManager, ViewType, build_appbar_actions

####################################################################################################
### Login View
####################################################################################################


def show_login_view(*, page: Page, api_client: ApiClient) -> None:

    text_field_username = TextField(label="Username", width=300)
    text_field_password = TextField(label="Password", width=300, password=True)

    wrong_username_password = AlertDialog(title=Text("Wrong username or password!"))

    def on_login_button_click(event: Event) -> None:
        username = text_field_username.value
        password = text_field_password.value

        user_api = UserApi(api_client=api_client)
        try:
            token: TokenSchema = user_api.api_v1_user_login_post(
                username=username,
                password=password,
            )
        except (UnauthorizedException, ApiException):
            page.dialog = wrong_username_password
            wrong_username_password.open = True
            page.update()

        else:
            encrypted_access_token = encrypt_client_storage_value(value=token.access_token)
            page.client_storage.set(key=CSK.AUTH_TOKEN, value=encrypted_access_token)

            page.session.set(SSK.USERNAME, username)
            api_client.configuration.access_token = token.access_token

            build_appbar_actions(page=page, api_client=api_client)
            ViewManager.show(ViewType.DASHBOARD)

    def on_back_button_click(event: Event) -> None:
        ViewManager.show(ViewType.LANDING)

    page.appbar.title = Text("HostYourDocs - Login")
    page.appbar.actions = [TextButton("Back", icon=icons.ARROW_BACK, on_click=on_back_button_click)]
    page.clean()

    page.add(
        Text("HostYourDocs Admin WebApp", size=30),
        text_field_username,
        text_field_password,
        ElevatedButton(text="Login", icon=icons.LOGIN, on_click=on_login_button_click),
    )

    page.update()
