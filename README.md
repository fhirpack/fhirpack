# FHIR Python Analysis and Conversion Kit (PACK)

FHIRPACK (FHIR Python Analysis Conversion Kit) is a general purpose package that simplifies the access, crawling, analysis and representation of FHIR and EHR data. FHIRPACK was designed and developed at Institute for Artificial Intelligence in Medicine ([IKIM](https://mml.ikim.nrw/)) and the Database Systems Research Group of the University of Heidelberg ([HDDBS](https://dbs.ifi.uni-heidelberg.de/)). 

## About this Project

The [FHIR](https://www.hl7.org/fhir/resourcelist.html) standard is a promising framework for interacting with healthcare data. However, tools for lightweight and efficient server communcation are lacking. FHIRPACK provides an easy-to-use and intuitive API that enables effortless access to FHIR data.

- **Website: read the docs**
- **Contact: email**
- **Tutorial: [notebooks](examples)**
- **Slack:** https://join.slack.com/t/fhirpack/shared_invite/zt-16f0dt3rr-76L6OKQIMOFbG2IKYnVLqA
- **Bug reports:**
- **Contributing: [CONTRIBUTING.rst](CONTRIBUTING.rst)**

## Installation

We strongly recommend using a virtual environment such as [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) or [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today).

Install the latest version of FHIRPACK:

```shell
pip install fhirpack
```

alternatively use pipenv:

```shell
pipenv install fhirpack
```

### Server configurations

To set your server configurtations, create an `.env` file in the root of the directory and specify settings as can be found in the example `.env.example` file. Alternatively, modify `.env.example` accorging to your needs.

**Note:** By Default, FHIRPACK connects to the public [http://hapi.fhir.org/baseR4](http://hapi.fhir.org/baseR4). We recommend using this setup to get familiar with the library.

## Simple Examples

### Get all conditions for a patient

In this example we extract all the conditions for a patient with the ID: `43fb1577-3455-41cf-9a07-c45aa5c0219e` from the public FHIR-server with the Base-URL: [http://hapi.fhir.org/baseR4](http://hapi.fhir.org/baseR4).

```python
>>> import fhirpack as fp
>>> pack = fp.PACK("http://hapi.fhir.org/baseR4")

>>> patient = pack.getPatients(["43fb1577-3455-41cf-9a07-c45aa5c0219e"]) # get the Patient by ID
>>> condition = patient.getConditions().explode() # extract all conditions for the patient
>>> condition.gatherText(lookUps=["display", "onsetDateTime", "reference"]) # display the specified FHIR elements of the conditions
```

### Get all patients with sepsis.

```python 
>>> import fhirpack as fp
>>> pack = fp.PACK("http://hapi.fhir.org/baseR4")

>> conditions = pack.getConditions(searchParams={"_content": "sepsis"}) # extract all conditions containing the word sepsis
>> patients = conditions.getPatients().explode() # get the respective patients
>> patients.gatherText(lookUps=["name", "address", "telecom", "birthDate"]) # display the specified FHIR elements of the patients
```

**Note:** For more examples and a deep-dive into FHIRPACK, please take a look at the [example jupyter notebooks](examples).

## CLI

FHIRPACK also provides a CLI for easy and quick data exploration.

The CLI can be invoked by using `python -m fhirpack.cli` or `fp`.

```shell
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

**Note:** Operations spanning mutliple spaces have to be quoted.

# Bugs

Please report any bugs that you find here or create a pull request accoring to the [contribution guidelines](CONTRIBUTING.rst).

---

# License

