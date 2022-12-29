# HostYourDocs

Host your static docs on your own infrastructure, easy, fast, and publicly accessible!

[![repository](https://img.shields.io/badge/src-GitLab-orange)](https://gitlab.com/DigonIO/hostyourdocs)
[![mirror](https://img.shields.io/badge/mirror-GitHub-orange)](https://github.com/DigonIO/hostyourdocs)
[![license](https://img.shields.io/badge/license-GPLv3-orange)](https://gitlab.com/DigonIO/hostyourdocs/-/blob/master/LICENSE)
[![Code style: black](https://gitlab.com/DigonIO/scheduler/-/raw/master/doc/_assets/code_style_black.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## WARNING: BETA VERSION

This is a prototype. HostYourDocs is not battle tested
and might exhibit unexpected behavior! HostYourDocs is currently undocumented and future changes in feature and behaviour may occur.

## Features

+ Static documentation hosting
+ Projects with versions and tags
+ Primary tag for SEO
+ Admin authentication
+ Project tokens (for CI/CD usage)
+ Injects a footer menu to each HTML
  + Easy navigation
  + Legal stuff: Impress & Privacy
+ Very simple webinterface

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
