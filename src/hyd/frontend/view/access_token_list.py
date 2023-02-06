from flet import (
    Column,
    Container,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Padding,
    Page,
    Row,
    Text,
    TextButton,
    colors,
)
from hyd_client import ApiClient
from hyd_client.api.token_api import TokenApi
from hyd_client.exceptions import ApiException, UnauthorizedException
from hyd_client.models.token_response_schema import TokenResponseSchema

####################################################################################################
### AccessTokenList View
####################################################################################################


def show_access_token_list_view(*, page: Page, api_client: ApiClient) -> None:
    page.appbar.title = Text("HostYourDocs - Access Tokens")
    page.clean()

    token_api = TokenApi(api_client=api_client)

    try:
        tokens: list[TokenResponseSchema] = token_api.api_v1_token_list_post()  # TODO should be get
    except (UnauthorizedException, ApiException) as err:
        print(err)
    else:
        page.add(
            build_api_token_data_table(
                tokens=[token for token in tokens if not token.is_login_token]
            ),
            build_login_token_data_table(
                tokens=[token for token in tokens if token.is_login_token]
            ),
        )

    page.update()


####################################################################################################
### Util
####################################################################################################


def build_api_token_data_table(*, tokens: list[TokenResponseSchema]) -> DataTable:
    token_table = DataTable(
        columns=[
            DataColumn(Text("ID"), numeric=True),
            DataColumn(Text("Project ID"), numeric=True),
            DataColumn(Text("Comment")),
            DataColumn(Text("Created")),
            DataColumn(Text("Expires")),
            DataColumn(Text("Status")),
        ],
        expand=True,
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
                    DataCell(TextButton(text="Revoke")),
                ]
            )
        )
    container = Container(
        width=1080,
        bgcolor=colors.SURFACE_VARIANT,
        padding=16,
        border_radius=8,
        content=Column(
            controls=[
                Text("API Token", size=32),
                Row(controls=[token_table]),
            ]
        ),
    )
    return container


def build_login_token_data_table(*, tokens: list[TokenResponseSchema]) -> DataTable:
    token_table = DataTable(
        columns=[
            DataColumn(Text("ID"), numeric=True),
            DataColumn(Text("Comment")),
            DataColumn(Text("Created")),
            DataColumn(Text("Expires")),
            DataColumn(Text("Status")),
        ],
        expand=True,
    )
    for token in tokens:
        token_table.rows.append(
            DataRow(
                cells=[
                    DataCell(Text(token.token_id)),
                    DataCell(Text(token.comment)),
                    DataCell(Text(token.created_at)),
                    DataCell(Text(token.expires_on)),
                    DataCell(TextButton(text="Revoke")),
                ]
            )
        )
    container = Container(
        width=1080,
        bgcolor=colors.SURFACE_VARIANT,
        padding=16,
        border_radius=8,
        content=Column(
            controls=[
                Text("Login Token", size=32),
                Row(controls=[token_table]),
            ]
        ),
    )
    return container
