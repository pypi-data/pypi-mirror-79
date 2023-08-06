# test-github-actions

Learn/test GitHub Actions for running CI/CD.

## Setting up GitHub Actions

To start, add a directory in your repo at `.github/workflows`. GitHub will
automatically detect this when it's pushed.

This directory is populated with YAML (`*.yml`) file that define different
automated workflows.

## Workflow YAML file syntax

A basic workflow definition file example:

```yaml
name: Build and Test

on:
  pull_request:
    branch:
      - master
  push:
    branch:
      - master

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run:
          python -m pip install --upgrade pip
          pip install black hypothesis pytest
      - name: Run tests
        run:
          python -m pytest
      - name: Check syntax
        run:
          black --check .
```

The `on` block defines what actions will trigger this workflow. In this
example the workflow will be triggered by either a push or a pull request to
the `master` branch.

The `jobs` block defines the workflow. Here we have one job called `ci`, which
is defined to run on the latest version of Ubuntu, and which consists of four
steps (which are run sequentially). Each step is given a (human-readable) `name`,
and a sequence of commands to run in the `run` block. The first two steps set
up the Python environment in which to run the tests, and then the latter two
steps use [PyTest](https://pytest.org) to run the provided unit tests, and
[Black](https://black.readthedocs.io/en/stable) to check the Python
formatting, respectively.

The `uses` lines bring in preset GitHub Actions; first to check out the
repository, which is defined at a level so that it is applied across all steps;
and, specifically in the 'Set up Python' step, a pre-defined Action is used to
make Python available.

## CI Matrix

Setting up a matrix allows you to run a job in parallel in multiple different
environments, e.g. operating systems, dependency versions, etc.

For example, rather than specifying a single OS via:

```yaml
ci:
  runs-on: ubuntu-latest
```

as above, the 'matrix' Strategy can be defined like so:

```yaml
ci:
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest]
  runs-on: ${{ matrix.os }}
```

so that the `ci` job is run on all of the specified operating systems.

The "matrix" of environments can have multiple dimensions; e.g. here we test
over a list of Python versions as well as over the list of operating systems:

```yaml
ci:
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest]
      python-version: [3.6, 3.7, 3.8]
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
```

## GitHub Secrets

GitHub allows you to create 'Secrets' (as long as your are an admin of the
repository), to supply workflows with confidential info like usernames and
passwords.

GitHub's docs say:

> Secrets are environment variables that are encrypted and only exposed to
> selected actions. Anyone with collaborator access to this repository can use
> these secrets in a workflow.
>
> Secrets are not passed to workflows that are triggered by a pull request from
> a fork.

Consider the following workflow, to publish a Python package to
[PyPI](https://pypi.org) (taken directly from the GitHub examples):

```yaml
# This workflows will upload a Python Package using Twine when a release is
# created

name: Upload Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python setup.py sdist bdist_wheel
        twine upload dist/*
```

Here it is clear in the 'Build and publish' step that the PyPI username and
password required for [Twine](https://twine.readthedocs.io/en/latest) to
upload the package to PyPI are contained in the `secrets` data structure that
GitHub makes available to the workflow.

On the menu bar of the repository, click 'Settings' and then click 'Secrets' in
the left pane.

## Caveats

- An individual job can be up to 6h long
- A workflow can be up to 72h long
- A matrix can contain up to 256 'columns'

## Creating Actions to share

A pre-made GitHub Action is just a Git repo. An example of the pre-defined
GitHub Actions is the `setup-python` action used in the above and found here:
<https://github.com/actions/setup-python>.

You can create your own generic GitHub actions and publish them for others to
use; all you need to do is define an `action.yml` file in the root of the
repository.

```yaml
name: "Generic Action to install <dependency>"
description: "A generic action to be shared on GitHub for other workflows to use"
branding:
  icon: ...
  color: "gray-dark"
inputs:
  <dependency>-version:
    description: "The version of <dependency> to install"
    required: true
    default: "1.0"
runs:
  using: ...
  steps:
    - run: |
        pip install <dependency>==${{ inputs.<dependency>-version }}
      shell: bash
```

To publish the Action, create a Release in the repository.

Other people can use this by adding:

```yaml
- uses: <GITHUB_USER>/<REPO_NAME>@master
```

## Links

- GitHub Actions: <https://github.com/features/actions>

- GitHub Actions docs (with yml definitions):
  https://docs.github.com/en/actions 
    - e.g. on how to create an action:
      <https://docs.github.com/en/actions/creating-actions>

- GitHub Actions Marketplace: <https://github.com/marketplace?type=actions> to
  browse existing solutions
