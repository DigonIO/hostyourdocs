import pytest
from starlette.testclient import TestClient

from hyd.backend.main import DeclarativeMeta, app, engine, init_db

DeclarativeMeta.metadata.drop_all(bind=engine)

####################################################################################################
#### Fixtures
####################################################################################################


@pytest.fixture
def client():

    init_db()

    yield TestClient(app)

    DeclarativeMeta.metadata.drop_all(bind=engine)


####################################################################################################
#### Util
####################################################################################################
