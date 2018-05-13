import json
import re
import copy
import sys

def geojson_write(geosjon, outfile_name):
	with open(outfile_name, 'w') as outfile:
		json.dump(geosjon, outfile, indent=2)
	print('end of osm2geojson')

# read the overpass data and separate into nodes and links
overpass_f = 'target_turin.osm'
data = json.load(open(overpass_f))
print(len(data))
elements = data['elements']
node_elements = []
way_elements = []
for e in elements:
	if e['type']=='node':
		node_elements.append(e)
	if e['type']=='way':
		way_elements.append(e)
print(elements[0])
print(node_elements[0])
print(way_elements[0])
print(len(elements), len(node_elements), len(way_elements))

# filter out the drivable links
pattern_drivable = "(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice)"
way_elements = [w_e for w_e in way_elements if re.search(pattern_drivable, w_e['tags']['highway'])]
print(len(elements), len(node_elements), len(way_elements))

feature_list = []
for n_e in node_elements:#[0:100]:
	n_f = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [n_e['lon'], n_e['lat']]}, "properties": {"color": [100, 100, 20, 155]}}
	feature_list.append(n_f)

node_dictionary = {n['id']:[n['lon'], n['lat']] for n in node_elements}
for w_e in way_elements:#[0:100]:
	w_f = {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [node_dictionary[w_e['nodes'][i]] for i in range(len(w_e['nodes']))]}, "properties": {"color": [10, 200, 20, 155]}}
	feature_list.append(w_f)

geojson = {"type": "FeatureCollection", "features": feature_list}
geojson_write(geojson, 'turin_full.json')
