from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    MainAxisAlignment,
    Page,
    Text,
    TextButton,
    icons,
)
from hyd_client import ApiClient
from hyd_client.api.project_api import ProjectApi
from hyd_client.exceptions import ApiException, UnauthorizedException
from hyd_client.models.project_response_schema import ProjectResponseSchema

####################################################################################################
### ProjectList View
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
