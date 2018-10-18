# ParchMint

Welcome to the ParchMint microfluidic benchmark repository. This is the current home of the ParchMint JSON validation schema, the set of known microfluidic benchmarks following that schema, and ongoing discussion about the evolution of the standard.

## Schema

We provide a JSON schema file that can be used to validate new ParchMint architecture files. The architecture files contain four top-level JSON keys: `layers`, `components`, `connections`, and `name`. The `name` key is simply a human readable name for your architecture. It is a required field, but is not required to be unique (although this is highly encouraged). The other top-level keys, and their members are described below.

### Layers

### Components

### Connections

## Benchmarks

The `benchmarks/` directory currently holds the following benchmarks:

### applicaiton-converted

* `planar_synthetic_1.json`
* `planar_synthetic_2.json`
* `planar_synthetic_3.json`
* `planar_synthetic_4.json`
* `planar_synthetic_5.json`
* `planar_synthetic_6.json`
* `planar_synthetic_7.json`

### assay-inspired

* `aquaflex-3b.json`
* `aquaflex-5a.json`
* `chromatin_immunoprecipitation.json`
* `general_purpose_mfd.json`
* `hiv1_p24_immunoassay.json`
* `molecular_gradients_generator.json`
