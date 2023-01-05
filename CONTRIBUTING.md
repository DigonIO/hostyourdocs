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

Create and activate a virtual environment:

```bash
python -m venv venv
source ./venv/bin/activate
```

Install the project with the development requirements and install
[pre-commit](https://pre-commit.com/) for the repository:

```bash
pip install -e .[dev]
python -m pre_commit install
```

To test changes made locally on your cloned repository, you can use the `build_docker.sh`
helper script to build updated docker images for your docker compose project:

```bash
./script/build_docker.sh
```

If you use the script for local development, use `hostyourdocs` instead of the
`registry.gitlab.com/digonio/hostyourdocs` url and `local` for the `<TAG>`
in the `docker-compose.yaml` file.

## Building the documentation

We are using Sphinx with [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)
formatting.

To build the documentation locally, run:

```bash
python -m sphinx -b html doc/ doc/_build/html
```
