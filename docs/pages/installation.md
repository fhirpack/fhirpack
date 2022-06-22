# Installation

You can easily install the latest FHIRPACK release from [PyPI](https://pypi.org/project/fhirpack/) or the most current version by cloning this repository. 
As usual with Python, we strongly recommend using virtual environments such as [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today), [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).

## Requirements

FHIRPACK requires Python 3.9 or greater as well as `libmagic` to work without problems. In case you're using an older Python version, you can use [asdf](https://asdf-vm.com/), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) or [pyenv](https://github.com/pyenv/pyenv) to have several Python versions coexist on your system. `libmagic` can be installed with `apt-get install libmagic-dev` on Ubuntu or `brew install libmagic` on MacOS.

## Using the Latest Release from PyPI


```shell
pip install fhirpack
```

alternatively use pipenv:

```shell
pipenv --python 3.9 install fhirpack
```

## Using the Latest Version a from Local Clone

```shell
git clone https://gitlab.com/fhirpack/main.git
mv main fhirpack
pip install -e fhirpack 
```

alternatively use pipenv:

```shell
git clone https://gitlab.com/fhirpack/main.git
mv main fhirpack
pipenv install -e fhirpack
```

## Configuration 

To set up a server configuration, create an `.env` file in the directory where you'll work with FHIRPACK and specify the settings as can be seen in [env.example](../../examples/.env.example). 
Alternatively, copy, rename and modify `.env.example` according to your needs.

:warning: By Default, FHIRPACK connects to the public R4 FHIR test server from HAPIFHIR [http://hapi.fhir.org/baseR4](http://hapi.fhir.org/baseR4). We recommend using this setup to get familiar with the library.
