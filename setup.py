from setuptools import setup

with open("src/hyd/__init__.py", "r") as file:
    content = file.read()
    co = compile(content, "header.py", "exec")
    version = co.co_consts[co.co_names.index("__version__")]
    author = co.co_consts[co.co_names.index("__author__")]


setup(
    name="hyd",
    version=version,
    author=author,
    python_requires=">=3.10",
    install_requires=[
        # "setuptools==65.5.0",
        "uvicorn==0.20.0",
        "fastapi==0.88.0",
        "pydantic==1.10.2",
        "sqlalchemy==1.4.35",
        "sqlalchemy2-stubs==0.0.2a29",
        "mariadb==1.0.11",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.5",
        "python-jose[cryptography]==3.3.0",
        "feedparser==6.0.3",
        "Jinja2==3.1.2",
        "flet==0.3.2",
    ],
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
