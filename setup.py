from enum import Enum

from setuptools import setup


class Dependecy(str, Enum):
    UVICORN = "uvicorn==0.20.0"
    FASTAPI = "fastapi==0.88.0"
    PYDANTIC = "pydantic==1.10.2"
    SQLALCHEMY = "sqlalchemy==1.4.35"
    SQLALCHEMY2_STUBS = "sqlalchemy2-stubs==0.0.2a29"
    MARIADB = "mariadb==1.0.11"
    PASSLIB_BCRYPT = "passlib[bcrypt]==1.7.4"
    PYTHON_MULTIPART = "python-multipart==0.0.5"
    PYTHON_JOSE_CRYPTOGRAPHY = "python-jose[cryptography]==3.3.0"
    FEEDPARSER = "feedparser==6.0.3"
    JINJA2 = "Jinja2==3.1.2"
    PRE_COMMIT = "pre-commit==2.20.0"
    TYPES_UJSON = "types-ujson==5.6.0.0"
    SPHINX = "Sphinx==5.2.3"
    M2R2 = "m2r2==0.3.3"
    NUMPYDOC = "numpydoc==1.5.0"
    FURO = "furo==2022.9.29"


Dep = Dependecy

REQ_INSTALL = {
    Dep.UVICORN,
    Dep.FASTAPI,
    Dep.PYDANTIC,
    Dep.SQLALCHEMY,
    Dep.MARIADB,
    Dep.PASSLIB_BCRYPT,
    Dep.PYTHON_MULTIPART,
    Dep.PYTHON_JOSE_CRYPTOGRAPHY,
    Dep.FEEDPARSER,
    Dep.JINJA2,
}

REQ_DEV = REQ_INSTALL | {
    Dep.PRE_COMMIT,
    Dep.SQLALCHEMY2_STUBS,
    Dep.TYPES_UJSON,
    Dep.SPHINX,
    Dep.M2R2,
    Dep.NUMPYDOC,
    Dep.FURO,
}

req_to_str_list = lambda req: [entry.value for entry in req]

setup(
    name="hyd",
    python_requires=">=3.10",
    install_requires=req_to_str_list(REQ_INSTALL),
    extras_require={
        "dev": req_to_str_list(REQ_DEV),
    },
    package_dir={"": "src"},
    package_data={
        "hyd": [
            "py.typed",
            "backend/templates/footer.html",
            "backend/templates/project.html",
            "backend/templates/simple.html",
            "backend/templates/loader.js",
        ]
    },
)
