from setuptools import setup

setup(
    name="hyd",
    python_requires=">=3.10.9",
    install_requires=[
        "uvicorn==0.18.2",
        "fastapi==0.88.0",
        "pydantic==1.10.2",
        "sqlalchemy==1.4.35",
        "mariadb==1.0.11",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.5",
        "python-jose[cryptography]==3.3.0",
        "feedparser==6.0.3",
        "Jinja2==3.1.2",
    ],
    extras_require={
        "dev": "pre-commit==2.20.0",
    },
    package_dir={"": "src"},
)
