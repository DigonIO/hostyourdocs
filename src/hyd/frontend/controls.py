import datetime as dt

from flet import Column, Container, Row, Text, TextButton, UserControl


class AccessTokenControl(UserControl):
    def __init__(
        self,
        *,
        token_id: int,
        project_id: int | None,
        comment: str,
        created_at: dt.datetime,
        expires_at: dt.datetime | None,
    ) -> None:
        super().__init__()
        self._token_id = token_id
        self._project_id = project_id
        self._comment = comment
        self._created_at = created_at
        self._expires_at = expires_at

    def build(self) -> None:

        row_meta = Row()
        column_meta = Column(
            [
                Text(self._comment, size=15),
                row_meta,
            ]
        )

        row_meta.controls.append(Text(f"Token ID: {self._token_id}"))
        if self._project_id:
            row_meta.controls.append(Text(f"Project ID: {self._project_id}"))
        row_meta.controls.append(Text(f"Created: {self._created_at}"))
        if self._expires_at:
            row_meta.controls.append(Text(f"Expires: {self._expires_at}"))

        return Row([column_meta, TextButton(text="Revoke")])
