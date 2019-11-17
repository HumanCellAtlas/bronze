# bronze

[![logo](./assets/logo.png?raw=true =250x250)](https://postimg.cc/image/fq2m11jcd/)

> _people used to make bronze [ancient bells](https://en.wikipedia.org/wiki/Bianzhong) as instruments and alarms in the early days._

We build `bronze` in this repo as:

- A library that talks to Slack API, Google Docs/Sheets API in a high-level and friendly way.
- A deployable and automated alarm service that sends reminders to Slack based on interpretable data files and Google Docs.

_Note: we started this project primaryly for HCA DCP deployment and notification automation purposes._

## Development
![Github](https://img.shields.io/badge/python-3.6+-green.svg?style=flat-square&logo=python&colorB=blue)
![GitHub](https://img.shields.io/github/license/HumanCellAtlas/bronze.svg?style=flat-square&colorB=blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

### Code style

The bronze code base is complying with the PEP-8 and using [Black](https://github.com/ambv/black) to 
format our code, in order to avoid "nitpicky" comments during the code review process so we spend more time discussing about the logic, not code styles.

In order to enable the auto-formatting in the development process, you have to spend a few seconds setting up the `pre-commit` the first time you clone the repo. It's highly recommended that you install the packages within a [`virtualenv`](https://virtualenv.pypa.io/en/latest/userguide/).

1. Install `pre-commit` by running: `pip install pre-commit` (or simply run `pip install -r requirements.txt`).
2. Run `pre-commit install` to install the git hook.

Once you successfully install the `pre-commit` hook to this repo, the Black linter/formatter will be automatically triggered and run on this repo. Please make sure you followed the above steps, otherwise your commits might fail at the linting test!

_If you really want to manually trigger the linters and formatters on your code, make sure `Black` and `flake8` are installed in your Python environment and run `flake8 DIR1 DIR2` and `black DIR1 DIR2 --skip-string-normalization` respectively._

## Deploy

Coming soon...
