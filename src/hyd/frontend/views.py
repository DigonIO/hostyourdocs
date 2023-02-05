from flet import (
    AlertDialog,
    AppBar,
    CircleAvatar,
    Column,
    Container,
    CrossAxisAlignment,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    ElevatedButton,
    Event,
    FloatingActionButton,
    Icon,
    IconButton,
    ListView,
    MainAxisAlignment,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Text,
    TextButton,
    TextField,
    VerticalDivider,
    colors,
    icons,
)
from hyd_client import ApiClient
from hyd_client.api.project_api import ProjectApi
from hyd_client.api.token_api import TokenApi
from hyd_client.api.user_api import UserApi
from hyd_client.exceptions import ApiException, UnauthorizedException
from hyd_client.models.project_response_schema import ProjectResponseSchema
from hyd_client.models.token_response_schema import TokenResponseSchema
from hyd_client.models.token_schema import TokenSchema

from hyd.frontend.controls import AccessTokenControl
from hyd.frontend.security import (
    decrypt_client_storage_value,
    encrypt_client_storage_value,
)
from hyd.frontend.storage_key import ClientStorageKey as CSK
from hyd.frontend.storage_key import SessionStorageKey as SSK

####################################################################################################
### Init View
####################################################################################################


def init_view(*, page: Page, api_client: ApiClient) -> None:
    encrypted_token = page.client_storage.get(CSK.AUTH_TOKEN)
    if encrypted_token is None:
        return show_landing_view(page=page, api_client=api_client)

    access_token: str = decrypt_client_storage_value(encrypted_value=encrypted_token)
    api_client.configuration.access_token = access_token

    user_api = UserApi(api_client=api_client)
    try:
        user_api.api_v1_user_greet_get_with_http_info()
    except (UnauthorizedException, ApiException):
        api_client.configuration.access_token = None
        show_landing_view(page=page, api_client=api_client)
    else:
        page.session.set(SSK.USERNAME, "admin")  # TODO request user meta data

        build_appbar_actions(page=page, api_client=api_client)
        show_dashboard_view(page=page, api_client=api_client)


####################################################################################################
### Landing Views
####################################################################################################


def show_landing_view(*, page: Page, api_client: ApiClient) -> None:
    def on_login_button_click(event: Event) -> None:
        show_login_view(page=page, api_client=api_client)

    page.appbar.title = Text("HostYourDocs")
    page.appbar.actions = [TextButton("Login", icon=icons.LOGIN, on_click=on_login_button_click)]
    page.clean()
    page.update()


####################################################################################################
### Login Views
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
            show_dashboard_view(page=page, api_client=api_client)

    def on_back_button_click(event: Event) -> None:
        show_landing_view(page=page, api_client=api_client)

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


####################################################################################################
### Dashboard Views
####################################################################################################


def show_dashboard_view(*, page: Page, api_client: ApiClient) -> None:
    page.appbar.title = Text("HostYourDocs - Dashboard")
    page.clean()

    page.add(
        Text("Hello admin", size=30),
        Text("TODO", size=30),
    )

    page.update()


####################################################################################################
### Project List Views
####################################################################################################


def show_project_list_view(*, page: Page, api_client: ApiClient) -> None:
    page.appbar.title = Text("HostYourDocs - Projects")
    page.clean()

    project_api = ProjectApi(api_client=api_client)

    try:
        projects: list[ProjectResponseSchema] = project_api.api_v1_project_list_get()
    except (UnauthorizedException, ApiException) as err:
        print(err)
    else:
        page.add(
            Container(
                content=Column(
                    [
                        TextButton(text="New Project", icon=icons.ADD),
                        build_project_data_table(projects=projects),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            )
        )

    page.update()


####################################################################################################
### Access Token Views
####################################################################################################


def show_access_token_view(*, page: Page, api_client: ApiClient) -> None:
    page.appbar.title = Text("HostYourDocs - Access Tokens")
    page.clean()

    token_api = TokenApi(api_client=api_client)

    try:
        tokens: list[TokenResponseSchema] = token_api.api_v1_token_list_post()  # TODO should be get
    except (UnauthorizedException, ApiException) as err:
        print(err)
    else:
        page.add(build_active_token_data_table(tokens=tokens))

    page.update()


####################################################################################################
### Util
####################################################################################################


def build_project_data_table(*, projects: list[ProjectResponseSchema]) -> DataTable:
    project_table = DataTable(
        columns=[
            DataColumn(Text("ID"), numeric=True),
            DataColumn(Text("Name")),
            DataColumn(Text("Created")),
            DataColumn(Text("Tags"), numeric=True),
            DataColumn(Text("Versions"), numeric=True),
        ]
    )
    for project in projects:
        project_table.rows.append(
            DataRow(
                cells=[
                    DataCell(Text(project.id)),
                    DataCell(Text(project.name)),
                    DataCell(Text(project.created_at)),
                    DataCell(Text(len(project.tags))),
                    DataCell(Text(len(project.versions))),
                ],
            )
        )
    return project_table


def build_active_token_data_table(*, tokens: list[TokenResponseSchema]) -> DataTable:
    token_table = DataTable(
        columns=[
            DataColumn(Text("ID"), numeric=True),
            DataColumn(Text("Project ID"), numeric=True),
            DataColumn(Text("Comment")),
            DataColumn(Text("Created")),
            DataColumn(Text("Expires")),
            DataColumn(Text("Action")),
        ]
    )
    for token in tokens:
        token_table.rows.append(
            DataRow(
                cells=[
                    DataCell(Text(token.token_id)),
                    DataCell(Text(token.project_id)),
                    DataCell(Text(token.comment)),
                    DataCell(Text(token.created_at)),
                    DataCell(Text(token.expires_on)),
                    DataCell(ElevatedButton(text="Revoke")),
                ]
            )
        )
    return token_table


def build_appbar_actions(*, page: Page, api_client: ApiClient) -> None:
    def on_dashboard_button_click(event: Event) -> None:
        show_dashboard_view(page=page, api_client=api_client)

    def on_projects_button_click(event: Event) -> None:
        show_project_list_view(page=page, api_client=api_client)

    def on_access_tokens_button_click(event: Event) -> None:
        show_access_token_view(page=page, api_client=api_client)

    def on_logout_button_click(event: Event) -> None:
        show_landing_view(page=page, api_client=api_client)

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
