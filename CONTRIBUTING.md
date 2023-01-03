# Contributing

Contributions to HostYourDocs are highly appreciated.

## Code of Conduct

When participating in this project, please treat other people respectfully.
Generally the guidelines pointed out in the
[Python Community Code of Conduct](https://www.python.org/psf/conduct/)
are a good standard we aim to uphold.

## Feedback and feature requests

We'd like to hear from you if you are using `HostYourDocs`.

For suggestions and feature requests feel free to submit them to our
[issue tracker](https://gitlab.com/DigonIO/hostyourdocs/-/issues).

## Bugs

Found a bug? Please report back to our
[issue tracker](https://gitlab.com/DigonIO/hostyourdocs/-/issues).

If possible include:

* Operating system name and version
* python and `HostYourDocs` version
* Steps needed to reproduce the bug

## Development Setup

**WARNING - Instructions Incomplete**

Clone the `HostYourDocs` repository with `git` and enter the directory:

```bash
git clone git@gitlab.com:DigonIO/hostyourdocs.git
cd hostyourdocs
```

### Using Docker

Make sure you have [docker](https://www.docker.com/) installed and the
[docker daemon](https://docs.docker.com/get-started/overview/) is running.

To test changes made locally on your cloned repository, you can use the `build_docker.sh`
helper script to build updated docker images for your docker compose project:

```bash
./script/build_docker.sh
```

If you use the script, use `hostyourdocs` for `<URL/ID>` and `local` for the `<TAG>`
in the `docker-compose.yaml` file. Alternatively our latest images can be found in the
[container registry](https://gitlab.com/DigonIO/hostyourdocs/container_registry/3759011).

Move the files from the `./docker` directory to wherever you want to manage the service from.
Then replace `<URL/ID>`, `<TAG>`, `<PORT>` and `<PATH>` according to your needs in the
`docker-compose.yaml` file.

Make sure to create the volumes required by the docker compose project:

```bash
# mkdir -p <PATH>/hyd/data_backend
# mkdir -p <PATH>/hyd/data_db
```

In the `envfiles/` directory create the environment files `backend.env`, `db.env`
and `shared.env` according to the given `envfiles/*.env.template` files.

The environment variables for the backend service `envfiles/backend.env`:

| variable         | required | info                              |,

| ---------------- | -------- | --------------------------------- |
| SECRET_KEY       | yes      | Hex string with at least 32 bytes |
| NAME_HOSTED_BY   | no       | Provider name                     |
| LINK_HOSTED_BY   | no       | Provider website URL              |
| LINK_IMPRESS     | no       | Provider impress URL              |
| LINK_PRIVACY     | no       | Provider privacy URL              |
| ROOT_PATH        | no       | Webserver root path for HYD       |

The environment variables for the mariadb database `envfiles/db.env`:

| variable              | required | info                                                      |
| --------------------- | -------- | --------------------------------------------------------- |
| MARIADB_ROOT_PASSWORD | yes      | See [dockerhub#mariadb](https://hub.docker.com/_/mariadb) |

The shared environment variables between the backend and database `envfiles/db.env`:

| variable              | required | info                                                      |
| --------------------- | -------- | --------------------------------------------------------- |
| MARIADB_PASSWORD      | yes      | See [dockerhub#mariadb](https://hub.docker.com/_/mariadb) |

With the variables declared, change to the directory containing your `docker-compose.yaml` and
start the compose project:

```bash
cd <docker-compose-dir>
docker compose up
```
