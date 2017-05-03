import json
import sys
import os.path
from glob import glob


pattern = os.path.join(sys.argv[1], '*.json')
placelog  = open("placelog.csv", "w")
routelog  = open("routelog.csv", "w")
for file_name in glob(pattern):
	print(file_name)
	with open(os.path.join(sys.argv[1],file_name)) as json_data:
		d = json.load(json_data)
		params = d["params"]
		width =  params["width"]
		height = params["height"]
		total_wire_length = params["total_wire_length"]
		avg_wire_length = params["avg_wire_length"]
		total_chip_area = params["total_chip_area"]
		used_area = params["used_area"]
		utilization = params["utilization"]
		text = file_name+","+"Y"+str(width)+","+str(height)+","+str(total_chip_area)+","+str(used_area)+","+str(utilization)+"\n"
		placelog.write(text)
		text = file_name+","+"Y"+","+str(total_wire_length)+","+str(avg_wire_length)+"\n"
		routelog.write(text)

		print("width: " , params["width"])
		print("height: " , params["height"])
		print("total_wire_length: " , params["total_wire_length"])
		print("avg_wire_length: " , params["avg_wire_length"])
		print("total_chip_area: " , params["total_chip_area"])
		print("used_area: " , params["used_area"])
		print("utilization: " , params["utilization"])

placelog.close()

