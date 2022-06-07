# FHIR Python Analysis and Conversion Kit (FHIRPACK)

FHIRPACK (FHIR Python Analysis Conversion Kit) is a general purpose package that simplifies the access, analysis and representation of FHIR and EHR data. FHIRPACK was designed and developed at Institute for Artificial Intelligence in Medicine ([IKIM](https://mml.ikim.nrw/)) and the Database Systems Research Group of the University of Heidelberg ([HDDBS](https://dbs.ifi.uni-heidelberg.de/)). 

## About FHIRPACK

The [FHIR](https://www.hl7.org/fhir/resourcelist.html) standard is a promising framework for interacting with healthcare data. However, tools for lightweight and efficient server communcation are lacking. FHIRPACK provides an easy-to-use and intuitive API that enables effortless access to FHIR data.

- **Tutorial: [Sample Jupyter Notebooks](examples)**
- **Documentation and Reference: [Read the Docs](https://fhirpack.readthedocs.io)**
- **Contact: jayson.salazar@uk-essen.de**
- **Questions, Discussions and Collaboration:** [Slack](https://join.slack.com/t/fhirpack/shared_invite/zt-16f0dt3rr-76L6OKQIMOFbG2IKYnVLqA)
- **Bug reports and Feature Requests:** preferrably on [our main GitLab tracker](https://gitlab.ume.de/fhirpack/main) or here on GitHub 
- **Contributing and Extending FHIRPACK: See [CONTRIBUTING.rst](CONTRIBUTING.rst)**

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

To set your server configurtations, create an `.env` file in the root of the directory and specify settings as can be seen in [.env.example](.env.example). Alternatively, copy, rename and modify `.env.example` according to your needs.

**Note:** By Default, FHIRPACK connects to the public [http://hapi.fhir.org/baseR4](http://hapi.fhir.org/baseR4). We recommend using this setup to get familiar with the library.

## Simple Examples

### Get all conditions for a patient

In this example we extract all the conditions for a patient with the ID: `43fb1577-3455-41cf-9a07-c45aa5c0219e` from the public FHIR-server with the Base-URL: [http://hapi.fhir.org/baseR4](http://hapi.fhir.org/baseR4).

```python
import fhirpack as fp # import FHIRPACK
pack = fp.PACK("http://hapi.fhir.org/baseR5") # instantiate a connected PACK for the specified FHIR API base 

patient = pack.getPatients(["43fb1577-3455-41cf-9a07-c45aa5c0219e"]) # retrieve a list of Patients of length one by ID
condition = patient.getConditions().explode() # retrieve all respective conditions for said patients
condition.gatherSimplePaths(["id", "code.coding.code", "code.coding.display", "onsetDateTime" ]) # gather and display the FHIR elements with the specified paths from the conditions
```

|	id	|code.coding.code	|code.coding.display	|onsetDateTime|	
|:--|:--|:--|:--|
|0	|`2a65f2a4-1a8d-46d9-a5f9-3af95a5d99bd`	|`[267036007]`	|`[Dyspnea (finding)]	`|`2020-02-23T12:07:58-06:00`|
|1	|`c9f11f99-796c-4c34-9a8e-246f1faa0039`	|`[840544004]`	|`[Suspected COVID-19]	`|`2020-02-23T12:07:58-06:00`|
|2	|`d5c30da3-546c-486c-bdb4-ff8f1b62a553`	|`[386661006]`	|`[Fever (finding)]	`|`2020-02-23T12:07:58-06:00`|
|3	|`a9c2b72d-b6de-4544-95d8-16246786fb5b`	|`[49727002] `   `|[Cough (finding)]	`|`2020-02-23T12:07:58-06:00`|
|4	|`dd0b2c03-75fe-4d2e-9d49-45c543f5c825`	|`[840539006]`	|`[COVID-19]		`|`2020-02-23T13:26:58-06:00`|

### Get all patients with sepsis.

```python 
import fhirpack as fp # import FHIRPACK
pack = fp.PACK("http://hapi.fhir.org/baseR5") # instantiate a connected PACK for the specified FHIR API base 

conditions = pack.getConditions(searchParams={"_content": "sepsis"}) # extract all conditions containing the word sepsis
patients = conditions.getPatients().explode() # get the respective patients
patients.gatherSimplePaths(["name.given", "name.family", "telecom.value", "address.country", "address.city", "birthDate"]) # display the specified FHIR elements of the patients
```

|	name.given	|name.family	|telecom.value	|address.country	|address.city	|birthDate|
|:--|:--|:--|:--|:--|:--|
|0	|`[[Herbert]]	`|`[Hoover]		`|`[8885551234]		`|`None	`|`[Everytown	`|` 1990-07-04`|
|1	|`[[Aaron697]]	`|`[Stiedemann542]	`|`[555-213-2064]	`|`[US]	`|`[Westford]	`|` 1946-03-29`|
|2	|`[[Aaron697]]	`|`[Stiedemann542]	`|`[555-213-2064]	`|`[US]	`|`[Westford]	`|` 1946-03-29`|
|3	|`[[Aaron697]]	`|`[Stiedemann542]	`|`[555-213-2064]	`|`[US]	`|`[Westford]	`|` 1946-03-29`|
|4	|`[[Aaron697]]	`|`[Stiedemann542]	`|`[555-213-2064]	`|`[US]	`|`[Westford]	`|` 1946-03-29`|
|5	|`[[Aaron697]]	`|`[Stiedemann542]	`|`[555-213-2064]	`|`[US]	`|`[Westford]	`|` 1946-03-29`|
|6	|`[[Charlesetta336], [Charlesetta336]]	`|`[Kihn564, Pouros728]	`|`[555-242-2559]	`|`[US]	`|`[Falmouth]`|`1943-12-17`|
|7	|`[[Hiram237]]	`|`[Kertzmann286]	`|`[555-171-6182]	`|`[US]	`|`[Fall River]	`|`1999-06-07`|
|11	|`[[Tim]]	`|`[Shabad]		`|`None			`|`None	`|`None		`|`1980-01-01`|

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

| Python | CLI |
| ------ | ------ |
| `pack.getPatients(["1"])` | `fp -o "getPatients 1"` |
| `pack.getPatients(["1", "181", "525"])` | `fp -o "getPatients 1, 181, 525"` |
| `PACK(envFile=".../env.example").getPatients(["1"])` | `fp -e .env.example -o "getPatients 1"` |
| `pack.getPatients(searchParams={}).gatherSimplePaths(["name.family"])` | `fp -o "getPatients" -p all -o "gatherSimplePaths name.family"` |
| `pack.getPatients(searchParams={"family":"Koepp"})` | `fp -o "getPatients" -p "family = Koepp"` |

**Note:** Operations spanning mutliple spaces have to be quoted.

# Bugs

Please report any bugs that you find here or create a pull request according to the [contribution guidelines](CONTRIBUTING.rst).

---

# License

Copyright (c) 2022 Jayson Salazar


