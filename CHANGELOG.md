# Changelog

## 0.2.1

### Misc

+ Add HYD project links to the injected footer.
+ Add title and version to swagger.
+ Start a documentation.
+ Add REST API testing.
+ Optimize the README.
+ Optimize the CI/CD pipeline.

## 0.2.0

### Feature

+ Tokens can be annotated with a comment.

### Misc

+ Add an installation guide to the `README.md`.
+ Add a `CONTRIBUTION.md` to the repository.

### Bugfix

+ `/api/token/create` no longer failing with `expires_on=None`.
+ Include missing `__init__.py` files.

## 0.1.6

### Bugfix

+ Include previously missing root_path in TemplateResponse.
+ Working footer with reverse proxy.

## 0.1.5

### Feature

+ Inject the footer loader script location into every html file at service start.

## 0.1.4

### Bugfix

+ Fix crashing thru unknown project ID while uploading a new version.
+ Fix project, tag, version deletion crash.

## 0.1.3

### Feature

+ Add the ROOT_PATH env var to the template file.
+ Complete the OpenAPI definition of the REST API.

### Bugfix

+ Add root path to links in HTML templates.

## 0.1.2

### Bugfix

+ Fix static file path in setup.py and PGK folder definition.

## 0.1.1

### Bugfix

+ Add missing static files.

## 0.1.0

+ Initial beta release
