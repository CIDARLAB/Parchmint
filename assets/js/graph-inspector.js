function updateD3() {
    var svg = d3.select("svg"),
        width = window.innerWidth, //+svg.attr("width"),
        height = window.innerHeight //+svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    svg.append("svg:defs").append("svg:marker")
        .attr("id", "triangle")
        .attr("refX", 15)
        .attr("refY", -1.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M 0 -5 10 10")
        .style("stroke", "black");

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) {
            return d.index;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));


    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("stroke-width", function(d) {
            return Math.sqrt(d.value);
        })
        .attr("marker-end", "url(#triangle)");

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(data.nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", function(d) {
            return color(d.group);
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


    node.append("title")
        .text(function(d) {
            return d.index;
        });

    var label = svg.selectAll(".nodelabels")
        .data(data.nodes)
        .enter()
        .append("text")
        .text(function(d) {
            return d.name;
        })
        .style("text-anchor", "middle")
        .style("fill", "#555")
        .style("font-family", "Arial")
        .style("font-size", 12);

    var edgelabel = svg.selectAll(".edgetext")
        .data(data.links)
        .enter()
        .append("text")
        .text(function(d) {
            return "src:" + d.sourcepin + "\n" + "tar:" + d.targetpin;
        })
        .style("text-anchor", "middle")
        .style("fill", "#555")
        .style("font-family", "Arial")
        .style("font-size", 12);

    simulation
        .nodes(data.nodes)
        .on("tick", ticked);


    simulation.force("link")
        .links(data.links)
        .distance(100);

    function ticked() {
        link
            .attr("x1", function(d) {
                return d.source.x;
            })
            .attr("y1", function(d) {
                return d.source.y;
            })
            .attr("x2", function(d) {
                return d.target.x;
            })
            .attr("y2", function(d) {
                return d.target.y;
            });

        node
            .attr("cx", function(d) {
                return d.x;
            })
            .attr("cy", function(d) {
                return d.y;
            });

        label.attr("x", function(d) {
                return d.x;
            })
            .attr("y", function(d) {
                return d.y - 10;
            });

        edgelabel
            .attr("x", function(d) {
                return d.source.x + (d.target.x - d.source.x) / 2;
            })
            .attr("y", function(d) {
                return d.source.y + (d.target.y - d.source.y) / 2;
            })

    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

}


var data = {
    "nodes": [],
    "links": []
}

var json;


function getIndexOfNode(list, itemtofind) {
    for (var index = 0; index < list.length; index++) {
        if (itemtofind == list[index].id) {
            return index;
        }
    }
}

function parseJSON(text) {
    json = JSON.parse(text);

    var components = json.components;
    var connections = json.connections;
    components.forEach(function(element) {
        data.nodes.push({
            "id": element.id,
            "entity": element.entity,
            "name": element.name
        });

    }, this);

    connections.forEach(function(connection) {
        var sourceindex = getIndexOfNode(components, connection.source.component);
        console.log("Source Index: " + sourceindex);
        var sourcepin = connection.source.port;
        console.log("Source pin: " + sourcepin);
        var targetpin;
        console.log("target pin: " + sourcepin);
        connection.sinks.forEach(function(sink) {
            targetindex = getIndexOfNode(components, sink.component);
            targetpin = sink.port
            data.links.push({
                "source": sourceindex,
                "target": targetindex,
                "sourcepin": sourcepin,
                "targetpin": targetpin
            });
        }, this);
    }, this);

    console.log("Number of connections: " + data.links.length);
    console.log(data.links);
    console.log("Number of components: " + data.nodes.length);
    console.log(data.nodes);
    updateD3();

}