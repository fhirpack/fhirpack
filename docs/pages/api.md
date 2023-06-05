# API

## Introduction

The structure of `FHIRPACK` can be divided into an [Extractor](./extractor.md), [Transformer](./transformer.md) and [Loader](./loader.md) according to the ETL philosophy. In addition, `FHIRPACK` uses [General](./general.md) methods that are not part of a specific pipeline component.

The [Extractor](./extractor.md) is responsible for retrieving [FHIR resources](https://www.hl7.org/fhir/resourcelist.html) from the server and storing them in the central [PACK](../api/fhirpack.pack.rst) object of `FHIRPACK`. Using methods provided by the [Transformer](./transformer.md), the data can be manipulated and analysed. Finally, the resulting data can be saved in various formats using the [Loader](loader.md).

```{toctree}
:maxdepth: 1
:caption: Content

General <general>
Extractor <extractor>
Transformer <transformer>
Loader <loader>
```

```{toctree}
:maxdepth: 1
:caption: Full Package

Fhirpack <../api/fhirpack>
```
