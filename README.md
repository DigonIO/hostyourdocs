# HostYourDocs

Host your docs on your own infrastructure, easy and secure!

[![repository](https://img.shields.io/badge/src-GitLab-orange)](https://gitlab.com/DigonIO/hostyourdocs)
[![mirror](https://img.shields.io/badge/mirror-GitHub-orange)](https://github.com/DigonIO/hostyourdocs)
[![license](https://img.shields.io/badge/license-GPLv3-orange)](https://gitlab.com/DigonIO/hostyourdocs/-/blob/master/LICENSE)
[![Code style: black](https://gitlab.com/DigonIO/scheduler/-/raw/master/doc/_assets/code_style_black.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## WARNING: BETA VERSION

This is a prototype. HostYourDocs is not battle tested
and might exhibit unexpected behavior! HostYourDocs is currently undocumented and future changes in feature and behaviour may occur.

## Features

+ Serve static docs and files
+ Organize projects with versions and tags
+ Authentication (currently admin only)
+ Project tokens (for CI/CD usage)
+ Minimal webinterface
+ Injects a footer menu to each HTML
  + Easy navigation
  + Legal stuff: Impress & Privacy

## Host Your Docs Using Docker Compose

Make sure you have [docker](https://www.docker.com/) installed and the
[docker daemon](https://docs.docker.com/get-started/overview/) is running.

### Get The Required Files

Copy the `docker-compose.yaml` file and the `envfiles/` folder from the `./docker`
directory in this repository to the desired path on your machine where you want to manage
the service from.
Then replace `<TAG>`, `<PORT>` and `<PATH>` according to your needs in the
`docker-compose.yaml` file.

For the variable `<TAG>` our latest images can be found in the
[container registry](https://gitlab.com/DigonIO/hostyourdocs/container_registry/3759011).

### Setup Environment Variables

In the `envfiles/` directory create the environment files `backend.env`, `db.env`
and `shared.env` according to the given `envfiles/*.env.template` files.
Setup the variables listed below according to your needs.

The environment variables for the backend service `envfiles/backend.env`:

| variable         | required | info                              |
| ---------------- | -------- | --------------------------------- |
| SECRET_KEY       | yes      | Hex string with at least 32 bytes |
| NAME_HOSTED_BY   | no       | Provider name                     |
| LINK_HOSTED_BY   | no       | Provider website URL              |
| LINK_IMPRESS     | no       | Provider impress URL              |
| LINK_PRIVACY     | no       | Provider privacy URL              |
| ROOT_PATH        | no       | Webserver root path for HYD       |

If you configure a root path, make sure to do the same for your reverse proxy.

The environment variables for the mariadb database `envfiles/db.env`:

| variable              | required | info                                                      |
| --------------------- | -------- | --------------------------------------------------------- |
| MARIADB_ROOT_PASSWORD | yes      | See [dockerhub#mariadb](https://hub.docker.com/_/mariadb) |

The shared environment variables between the backend and database `envfiles/db.env`:

| variable              | required | info                                                      |
| --------------------- | -------- | --------------------------------------------------------- |
| MARIADB_PASSWORD      | yes      | See [dockerhub#mariadb](https://hub.docker.com/_/mariadb) |

### Create Docker Volumes

Make sure to create the volumes required by the docker compose project:

```bash
# mkdir -p <PATH>/hyd/data_backend
# mkdir -p <PATH>/hyd/data_db
```

### Start HostYourDocs

Execute the follow command from the directory with the HostYourDocs `docker-compose.yaml` file:

```bash
docker compose up
```

## Open Endpoints

+ List all projects
  + `<protocol>://<address>:/<root_path>/simple`
+ Project information
  + `<protocol>://<address>:/<root_path>/simple/<project_name>`
+ Path to specific documentation tag
  + `<protocol>://<address>:/<root_path>/api/v1/<project_name>/t/<tag>`
+ Path to specific documentation version
  + `<protocol>://<address>:/<root_path>/api/v1/<project_name>/v/<version>`
+ Swagger
  + `<protocol>://<address>:/<root_path>/docs`

## License

This free and open source software (FOSS) is published under the
[GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
