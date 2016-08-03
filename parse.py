#trees density per mile in San Francisco

import csv
import geojson
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

data_file = "Street_Tree_List.csv"

#get the first 20 lines from the file
# with open(data_file) as myfile:
# 	head = [next(myfile) for x in range(50)]
# print(head)

#print out the species and location of the first 20 trees
with open(data_file) as myfile:
	#skip over header row
	next(myfile)
	csv_data = csv.reader(myfile, delimiter=",")
	trees = pd.DataFrame([next(csv_data) for x in range(8000)])

#TreeID,qLegalStatus,qSpecies,qAddress,SiteOrder,qSiteInfo,PlantType,qCaretaker,qCareAssistant,PlantDate,DBH,PlotSize,PermitNotes,XCoord,YCoord,Latitude,Longitude,Location


# Define type of GeoJSON we're creating
geo_map = {"type": "FeatureCollection"}

# Define empty list to collect each point to graph
tree_list = []

# Iterate over our data to create GeoJSOn document.
# Use iterrows to get make the Dataframe iterable
for index, line in trees.iterrows():
	#check if lat entry is empty
	if line[15] == "":
		continue

	# Setup a new dictionary for each iteration.
	data = {}

	# Assign line items to appropriate GeoJSON fields.
	data['type'] = 'Feature'
	data['id'] = str(index)
	data['properties'] = {'title': line[2]}
	data['geometry'] = {'type': 'Point',
						'coordinates': (line[16], line[15])}

	# Add data dictionary to tree_list
	tree_list.append(data)

# for point in tree_list:
#         geo_map.setdefault('features', []).append(point)

# with open('file_sf_trees.geojson', 'w') as f:
#         f.write(geojson.dumps(geo_map))

#define the border coordinates

left_most = -122.517600
right_most = -122.357129
top_most = 37.810950
bottom_most = 37.708054

coor_bl = [bottom_most, left_most]
coor_tl = [top_most, left_most]
coor_br = [bottom_most, right_most]
coor_tr = [top_most, right_most]

#define the bins into which to categorize each of the trees
def grid(top, left, bottom, right, bins):
	long_bin = abs((top-bottom)/bins)
	lat_bin = abs((left-right)/bins)

	#categorize tress into each bin, which will be a 2D array. sort the data set and split it on each bin
	count = 0
	for x in range(bins+1):
		print("long range: " + str(bottom+long_bin*count))
		print("lat range: " + str(left+lat_bin*count))
		count += 1



print(grid(top_most,left_most,bottom_most,right_most,10))
trees.sort(columns=[15], ascending=False, inplace=True)
print(trees.head())

#count the number in each bin

#define the color scale and how much to add to a given color based on number of trees

#give a color attribute to each bin, with intensity of color dependent on number of trees



# plt.show()



