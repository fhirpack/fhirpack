# FHIR Python Analysis and Conversion Kit (PACK)

FHIRPACK (FHIR Python Analysis Conversion Kit) is a general purpose package that simplifies the access, crawling, analysis and representation of FHIR and EHR data. FHIRPACK was designed and developed at Institute for Artificial Intelligence in Medicine ([IKIM](https://mml.ikim.nrw/)) and the Database Systems Research Group of the University of Heidelberg ([HDDBS](https://dbs.ifi.uni-heidelberg.de/)). 

## About this Project

FHIR is a promising framework for interacting with healthcare data. However, tools for lightweight and efficient server communcation are lacking. To fill this gap, FHIRPACK provides an easy-to-use and intuitive API that enables effortless access to FHIR data.

## Installation

We strongly recommend using a virtual environment such as venv, conda or pipenv. If you need help with this take a look at the [Setting up a virtual environment](#Setting-up-a-virtual-environment) section.

To install the package, run:

```shell
pip install fhirpack
```

### Setting up a virtual environment

## Usage

## Contributing

Describe how to contribute.

### Issues

Describe how to open issues, who to assign them to, what goes where, etc.

### Merge Requests

Describe how to open MRs, who to assign them to, what goes where, etc.

---

# Architecture

Describe the architecture of the project and add an architecture diagram.

## Stack

Describe the stack components in detail

### Dependencies

For more information, see our [Pipfile](Pipfile)

---

# Development

## Setup

Clone this repository

```shell
git clone ssh://git@git-dbs.ifi.uni-heidelberg.de:2222/main/lib-fhirpack.git
```

Install your virtual environment

```shell
pip install pipenv python-dotenv tox pipenv-setup
pipenv install --dev
```

Verify you can run the tests and build FHIR PACK via `tox`

```shell
tox -e; tox -e build; tox -e clean
```

Verify you can run the tests and execute FHIR PACK via your virtual environment

```shell
pipenv run pytest --mypkg fhirpack
```

```shell
pipenv run ptw --runner "pytest --testmon"
```

In some cases, tox can have problems installing dependencies, you can recreate the environment used by tox (under ./tox) by using `tox --recreate -e py3096`

## Dependencies

This project only relies on pyenv or asdf, pipenv, pipenv-setup, python-dotenv, pytest, pytest-watch, pytest-picked, pytest-testmon, bump2version and tox for development, testing, building and publishing

| Tool                                                                   | Rationale                                                    |
| ---------------------------------------------------------------------- | ------------------------------------------------------------ |
| [pyenv](https://github.com/pyenv/pyenv) or [asdf](http://asdf-vm.com/) | managing multiple python versions                            |
| [pipenv](https://github.com/pypa/pipenv)                               | managing virtual environments and seemless environment setup |
| [tox](https://github.com/tox-dev/tox)                                  | one single tool for testing, packaging and publishing        |
| [pytest](https://github.com/pytest-dev/pytest)                         | running unit tests                                           |
| [pytest-picked](https://github.com/anapaulagomes/pytest-picked)        | running only unit tests of code that has been changed        |
| [pytest-watch](https://github.com/joeyespo/pytest-watch)               | run unit tests continuously                                  |
| [python-dotenv](https://pypi.org/project/python-dotenv/)               | use `.env` variables within `tox.ini` seemlesly              |
| [pipenv-setup](https://github.com/Madoshakalaka/pipenv-setup)          | automatically populate Python's `setup.py` requirements      |
| [bump2version](https://github.com/c4urself/bump2version/)              | simple version management                                    |

## Jupyter Notebook

You can use Jupyter, JupyterLab or VSCode's Jupyter Plugin to use and improve `usage.py` and `samples.py`.
However, keep in mind to not upload notebook outputs as they bloat the files and are irrelevant to the reader.
To prevent that, execute `echo -e '[filter "strip-notebook-output"]\n\tclean = jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR' >> .git/config` within the repository.
That line defines a clean for Jupyter notebooks that git can then use for all `.ipynb` files as described in [.gitattributes](.gitattributes)

## VS Code

`tox -e clean`

---

# Testing

`pipenv run pytest tests`

`ptw --runner "pytest --testmon"`

`tox`

`pipenv run pytest -s --use-running-containers --docker-compose-no-build --pyargs fhirpack tests`

`ptw -- -s --use-running-containers --docker-compose-no-build --pyargs fhirpack tests -m 'not reqdocker'`

# Releasing

`bumpversion --allow-dirty patch ; cat VERSION`

https://peps.python.org/pep-0440/#final-releases

`tox -e build`

`tox -e publish`

---

# Usage

### CLI

The CLI can be invoked by using `python -m fhirpack.cli` or `fp`.

```
> fp --help                                
Usage: fp [OPTIONS]

  The pack for your FHIR server.

Options:
  --version               Show the version and exit.
  -s, --source TEXT       URL of the FHIR server or path to json files.
  -e, --environment TEXT  Path to Dotenv file containing configurations.
  -d, --destination TEXT  Location of the output.
  -o, --operation TEXT    Operations to retrieve data.
  -p, --params TEXT       Provide additional search parameters.
  -v, --verbose           Print results in verbose format.
  -h, --help              Show this message and exit.
```

CLI usage is analogous to the general `fhirpack` dataflow.

| python | shell |
| ------ | ------ |
| `pack.getPatients(["1"])` | `fp -o "getPatients 1"` |
| `pack.getPatients(["1", "181", "525"])` | `fp -o "getPatients 1, 181, 525"` |
| `PACK(envFile=".../env.example").getPatients(["1"])` | `fp -e .env.example -o "getPatients 1"` |
| `pack.getPatients(searchParams={}).gatherSimplePaths(["name.family"])` | `fp -o "getPatients" -p all -o "gatherSimplePaths name.family"` |
| `pack.getPatients(searchParams={"family":"Koepp"})` | `fp -o "getPatients" -p "family = Koepp"` |

Of note, operations spanning mutliple spaces have to be quoted.

### Python with .env File

```
client=fp.utils.clientFromEnv()
pack= fp.pack.PACK(client)
```

### Python with Manual Client Definition

```
import fhirpy
client = fhirpy.SyncFHIRClient("http://127.0.0.1:32112/hapi-fhir-jpaserver/fhir/")
pack  = fp.pack.PACK(client)
pack.getPatient('1').to_resource().serialize()
```

---

# References

List any important or related reading material

---

# Acknowledgements

Acknowledge contributors
