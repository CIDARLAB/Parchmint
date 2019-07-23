# ParchMint

Welcome to the ParchMint microfluidic benchmark repository. This is the current home of the ParchMint JSON validation schema, the set of known microfluidic benchmarks following that schema, and ongoing discussion about the evolution of the standard.

## Schema

We provide a JSON schema file that can be used to validate new ParchMint architecture files. The architecture files contain five top-level JSON keys: `layers`, `components`, `connections`, `features`, and `name`. The `name` key is simply a human readable name for your architecture. It is a required field, but is not required to be unique (although this is highly encouraged). The other top-level keys, and their members are described below.

### Layers

The `layers` key contains an array of layer ojects. Each individual layer object contains a unique id string `id` and a human readable name string `name`.

```json
"layers": [
    {
        "id": "unique-flow-layer-id-string",
        "name": "flow-layer"
    },
    {
        "id": "unique-control-layer-id-string",
        "name": "control-layer"
    }
]
```

### Components

The `components` key contains an array of component objects which represent all the unplaced components in your microfluidic device. Each individual component object contains a unique id string `id` and a human readable name string `name`. The component object also contains a number of keys which represent the components physical presence such as the `layers` key, which is an array of layer id's representing which layers this component exists on, the `x-span` and `y-span` integer keys which represent the the amount of space the component's bounding box takes in the x and y directions, respectively, and the `entity` string key which represents what type of component this component object represents. Finally the component object contains a `ports` key which contains an array of port objects. Each port object has a `label` string key which is similar to a unique id but is only required to be unique within that port list (this allows you to re-use the same port names between the same components), a `layer` string key which signifies which layer the port is located on (and should be one of the layers listed in the component object's layer list), and an `x` and `y` integer key which represents the ports x and y direction offset relative to the upper left of the component objects bounding box (making this port location relative to the component). Because this architecture system assumes zero knowledge of the component internals, ports should only exist at the edge of the component bounding box.

```json
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

The `connectors` key contains an array of connection objects which represent all the unrouted connections in your microfluidic device. Each individual connection object contains a unique id string `id` and a human readable name string `name`. The connection object contains a `layer` key which is the layer id for the layer this connection exists on and a `source` and `sinks` key. The `source` and `sinks` keys each contain terminal objects, with the `source` containing a single terminal object and the `sinks` containing an array of terminal objects to allow for the representation of multinets. Each terminal object contains a `component` key which is a component id and represents which component this connecitons starts or ends at and an optional `port` key which represents which port on that component this connection uses if a specific port is required.

```json
"connections": [
    {
        "id": "unique-mixer-flow-connection-id",
        "name": "mixer-flow-connection",
        "layer": "unique-flow-layer-id-string",
        "source": {
            "component": "unique-mixer-id-string",
            "port": "input-port"
        },
        "sinks": [
            {
                "component": "unique-output-id-string",
                "port": "io-port"
            }
        ]
    }
]
```

### Features

The `features` key contains two different types of objects; component features which represent the placed information for a component for analysis and fabrication, and connection features which represent a straight line route segment of a connection.

#### Component Feature

The component feature contains `name`, `id`, and `layer` fields which should match the `name` and `id` field of the abstract component in the `components` array that it represents and one of the layers in the abstract components layers list. It should also contain a `location` object which contians `x` and `y` keys with the integer location of the component bounding boxes upper left point and a `x-span` and `y-span` keys which represent the size of the bounding box, and a `depth` key representing how deep the component should be.

```json
"features": [
    {
        "name": "mixer-001",
        "id": "unique-mixer-id-string",
        "layer": "unique-flow-layer-id-string",
        "location": {
            "x": 500,
            "y": 2000
        },
        "x-span": 4500,
        "y-span": 1500,
        "depth": 10
    }
]
```

#### Connection Feature

The connection feature contains an `id` field which should be a unique id string and a `name` field which should be a human readable name. It also contains a `connection` key which should be the id of the connection that this connection feature is a straight line segment of and a `layer` which should match the layer that that connection is supposed to be routed on unless this connection utilizes through-layer vias. It contains `width` and `depth` keys which represent the width of the channel tangentially to its direction of travel and its channel depth, respectively, as well as `source` and `sink` keys, which each contain a single object with `x` and `y` keys represent each end of this straight line segment. Finally, it contains a `type` key which currently is always set to `"channel"`.

```json
"features": [
    {
        "name": "mixer-flow-connection-segment-001",
        "id": "unique-channel-segment-id",
        "connection": "unique-mixer-flow-connection-id",
        "layer": "unique-flow-layer-id-string",
        "width": 5,
        "depth": 10,
        "source": {
            "x": 500,
            "y": 2750
        },
        "sink": {
            "x": 50,
            "y": 2750
        },
        "type": "channel"
    }
]
```

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
