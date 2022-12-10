from setuptools import setup

setup(
    name="hyd",
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.68.1",
        "passlib[bcrypt]>=1.7.4",
        "sqlalchemy>=1.4.35",
        "python-multipart>=0.0.5",
        "mariadb>=1.0.11",
        "pydantic>=1.8.2",
        "python-jose[cryptography]>=3.3.0",
        "feedparser>=6.0.3",
        "uvicorn>=0.18.2",
    ],
    package_dir={"": "src"},
)
