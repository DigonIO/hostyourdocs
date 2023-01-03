"""
Generate an `openapi.json` without the need of a running backend service.
"""

from hyd.tooling import generate_openapi_json

if __name__ == "__main__":
    generate_openapi_json()
