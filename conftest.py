import pytest
from starlette.testclient import TestClient

from hyd.backend.main import DeclarativeMeta, app, engine

DeclarativeMeta.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    yield TestClient(app)

    DeclarativeMeta.metadata.drop_all(bind=engine)
    DeclarativeMeta.metadata.create_all(bind=engine)
