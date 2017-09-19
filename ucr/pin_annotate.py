import sys
import json
import os

# Function to check if a given point resides on the edges of a given component
def belongs_to(point, comp, size):
	if point[1] >= comp[1] and point[1] <= comp[1] + size[1]:
		if point[0] == comp[0] or point[0] == comp[0] + size[0]:
			return True
	if point[0] >= comp[0] and point[0] <= comp[0] + size[0]:
		if point[1] == comp[1] or point[1] == comp[1] + size[1]:
			return True
	return False

# Read the input file into the json data
filepath = "general_purpose_mfd.json" #sys.argv[1]
f = open(filepath)
data = json.load(f)
f.close()

# Initialize the entities port locations so we can re-assocaite them later
entities = {} # Entity map to ports for re-numbering
for dirName, subDirList, fileList in os.walk(os.path.join('.','entities')):
	for fileName in fileList:
		if fileName.endswith('.json'):
			print('Parsing: ' + fileName)
			f = open(os.path.join(dirName, fileName))
			data = json.load(f)
			f.close()
			print('Component Name: ' + data['component'])
			entities[data['component']] = {}
			for index,port in enumerate(data['flowPorts']['locations']):
				print(str(port['x']) + ',' + str(port['y']))
				entities[data['component']][str(port['x']) + ',' + str(port['y'])] = index

connections = []
components = []

entity_key = {} # keys the component name to it's entity type
sources = {} # (x,y) tuple
sinks = {} # (x,y) tuple
locations = {} # (x,y) tuple
size = {} # (width, height) tuple

# Collect all the sources and sinks for each connection, and all the connection ids
for conn in data["connections"]:
	sources[conn["id"]] = conn["source"]
	sinks[conn["id"]] = conn["sinks"]
	connections.append(conn["id"])

# Print the number of connections for debugging
print("Number of connections: " + str(len(connections)))

# Collect all the component ids for reference when getting the component locations
for comp in data["components"]:
	components.append(comp["id"])
	entity_key[comp['id']] = comp['entity']

# Print the number of components for debugging
print("Number of components: " + str(len(components)))

source_segments = {}
sink_segments = {}

# Create empty sets for the sources and sinks for each connection id
for conn in connections:
	source_segments[conn] = set()
	sink_segments[conn] = set()

# For each connection, put the source and sink points into the appropriate sets. Also collect the
# component locations so they can be subtracted from the source/sink to get the relative location
for feat in data["features"]:
	if "type" in feat and feat["type"] == "channel":
		source_segments[feat["params"]["connection"]].add( (feat["params"]["source"]["x"], feat["params"]["source"]["y"]) )
		sink_segments[feat["params"]["connection"]].add( (feat["params"]["sink"]["x"], feat["params"]["sink"]["y"]) )
	else:
		locations[feat["id"]] = (feat["params"]["location"]["x"], feat["params"]["location"]["y"])
		size[feat["id"]] = (feat["params"]["width"], feat["params"]["height"])

# Check if there is a disparity between the number of sources and the number of sinks
# both the source and sink should have one extra point, which will make them equal
for conn in connections:
	if len(source_segments[conn]) != len(sink_segments[conn]):
		print("Source and sink size mismatch on: " + conn + "\n\tsource_segments: " + str(len(source_segments)) + "\n\tsink_segments: " + str(len(sink_segments)))

# Get the extra point of the sources and the extra point of the sinks
for conn in connections:
	source_minus_sink = source_segments[conn] - sink_segments[conn]
	sink_minus_source = sink_segments[conn] - source_segments[conn]
	print(conn + "\n\tsource - sink: " + str(source_minus_sink) + "\n\tsink - source: " + str(sink_minus_source))

	# Find the correct component for the source and the sink points (seperated for debugging)
	# Subtract the component's upper left point from the source/sink point to get the relative position
	# Write that relative position back to the object
	for comp in components:
		if belongs_to(list(source_minus_sink)[0], locations[comp], size[comp]):
			print("\tSource belongs to: " + comp + " at " + str(locations[comp]) + " of " + str(size[comp]))
			tup = (list(source_minus_sink)[0][0] - locations[comp][0], list(source_minus_sink)[0][1] - locations[comp][1])
			print("\t\tRelative Location: " + str(tup))
			for c in data["connections"]:
				if c["source"] == comp:
					if "params" not in c:
						c["params"] = {}
					c["params"]["source_pin"] = {}
					c["params"]["source_pin"] = entities[entity_key[comp]][str(tup[0]) + ',' + str(tup[1])]
					print('\t\tPin Number: ' + str(c['params']['source_pin']))
					#c["params"]["source_pin"]["x"] = tup[0]
					#c["params"]["source_pin"]["y"] = tup[1]
				else:
					if "params" not in c:
						c["params"] = {}
					c["params"]["sink_pin"] = {}
					c["params"]["sink_pin"] = entities[entity_key[comp]][str(tup[0]) + ',' + str(tup[1])]
					print('\t\tPin Number: ' + str(c['params']['sink_pin']))
					#c["params"]["sink_pin"]["x"] = tup[0]
					#c["params"]["sink_pin"]["y"] = tup[1]

	for comp in components:
		if belongs_to(list(sink_minus_source)[0], locations[comp], size[comp]):
			print("\tSink belongs to: " + comp + " at " + str(locations[comp]) + " of " + str(size[comp]))
			tup = (list(sink_minus_source)[0][0] - locations[comp][0], list(sink_minus_source)[0][1] - locations[comp][1])
			print("\t\tRelative Location: " + str(tup))
			for c in data["connections"]:
				if c["source"] == comp:
					if "params" not in c:
						c["params"] = {}
					c["params"]["source_pin"] = {}
					c["params"]["source_pin"] = entities[entity_key[comp]][str(tup[0]) + ',' + str(tup[1])]
					print('\t\tPin Number: ' + str(c['params']['source_pin']))
					#c["params"]["source_pin"]["x"] = tup[0]
					#c["params"]["source_pin"]["y"] = tup[1]
				else:
					if "params" not in c:
						c["params"] = {}
					c["params"]["sink_pin"] = {}
					c["params"]["sink_pin"] = entities[entity_key[comp]][str(tup[0]) + ',' + str(tup[1])]
					print('\t\tPin Number: ' + str(c['params']['sink_pin']))
					#c["params"]["sink_pin"]["x"] = tup[0]
					#c["params"]["sink_pin"]["y"] = tup[1]

# Re-dump the updated object to a file
outfilepath = filepath+ _pin_assiged.json
w = open(outfilepath,"w")
json.dump(data, w, indent=4)
w.close()
