# ParchMint

Welcome to the ParchMint microfluidic benchmark repository. This is the current home of the ParchMint JSON validation schema, the set of known microfluidic benchmarks following that schema, and ongoing discussion about the evolution of the standard.

## Schema

We provide a JSON schema file that can be used to validate new ParchMint architecture files. The architecture files contain five top-level JSON keys: `layers`, `components`, `connections`, `features`, and `name`. The `name` key is simply a human readable name for your architecture. It is a required field, but is not required to be unique (although this is highly encouraged). The other top-level keys, and their members are described below.

### Layers

The `layers` key contains an array of layer ojects. Each individual layer object contains a unique id string `id` and a human readable name string `name`.

```
"layers": [
    {
        "id": "unique-flow-layer-id-string",
        "name": "flow-layer"
    },
    {
        "id": "unique-control-layer-id-string",
        "name": "control-layer"
    },
]
```

### Components

The `components` key contains an array of component objects. Each individual component object contains a unique id string `id` and a human readable name string `name`. The component object also contains a number of keys which represent the components physical presence such as the `layers` key, which is an array of layer id's representing which layers this component exists on,the `x-span` and `y-span` integer keys which represent the the amount of space the component's bounding box takes in the x and y directions, respectively, and the `entity` string key which represents what type of component this component object represents. Finally the component object contains a `ports` key which contains an array of port objects. Each port object has a `label` string key which is similar to a unique id but is only required to be unique within that port list (this allows you to re-use the same port names between the same components), a `layer` string key which signifies which layer the port is located on (and should be one of the layers listed in the component object's layer list), and an `x` and `y` integer key which represents the ports x and y direction offset relative to the upper left of the component objects bounding box (making this port location relative to the component). Because this architecture system assumes zero knowledge of the component internals, ports should only exist at the edge of the component bounding box.

```
"components": [
    {
        "id": "unique-mixer-id-string",
        "name": "mixer-001",
        "layers": [
            "unique-flow-layer-id-string",
            "unique-control-layer-id-string"
        ],
        "x-span": 4500,
        "y-span": 1500,
        "entity": "rotary-mixer",
        "ports": [
            {
                "label": "input-port",
                "layer": "unique-flow-layer-id-string",
                "x": 0,
                "y": 750
            },
            {
                "label": "output-port",
                "layer": "unique-flow-layer-id-string",
                "x": 4500,
                "y": 750
            },
            {
                "label": "rotary-control-port",
                "layer": "unique-control-layer-id-string",
                "x": 2250,
                "y": 0
            }
        ]
    }
]
```

### Connections

```
"connections": [
    {

    }
]
```

### Features

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