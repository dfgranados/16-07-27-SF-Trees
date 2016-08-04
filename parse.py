#trees density per mile in San Francisco
#data source: https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq

import csv
import geojson
import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.nan)
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


# Iterate over our data to create GeoJSOn document.
# Use iterrows to get make the Dataframe iterable
def create_geojson(dframe):
	# Define empty list to collect each point to graph
	tree_list = []

	for index, line in dframe.iterrows():
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

	for point in tree_list:
	        geo_map.setdefault('features', []).append(point)

	with open('file_sf_trees.geojson', 'w') as f:
	        f.write(geojson.dumps(geo_map))


#define the border coordinates
left_most = -122.517600
right_most = -122.357129
top_most = 37.810950
bottom_most = 37.708054

coor_bl = [bottom_most, left_most]
coor_tl = [top_most, left_most]
coor_br = [bottom_most, right_most]
coor_tr = [top_most, right_most]

#sort columns by longitude
trees.sort_values([15], ascending=False, inplace=True)
#convert values in the coordinate columns to floats. Coerce errors to NaN
# trees[15] = pd.to_numeric(trees[15], errors='coerce')
trees[[15,16]] = trees[[15,16]].apply(pd.to_numeric)

#define the bins into which to categorize each of the trees
def grid(top, left, bottom, right, num_bins):
	long_bin = abs((top-bottom)/num_bins)
	lat_bin = abs((left-right)/num_bins)

	count = 0
	bin_bound = []
	for x in range(num_bins+1):
		long_coor = bottom+long_bin*count
		lat_coor = left+lat_bin*count
		bin_bound.append([long_coor,lat_coor])
		count += 1

	#categorize tress into each bin, which will be a 2D array
	#use subsets to split trees dataframe
	lat_grid = []
	for x in range(num_bins):
		lat_grid.append(trees[(trees[15] >= bin_bound[x][0]) & ( trees[15] < bin_bound[x+1][0])])

	#THE DATA IS SPLIT ALONG ONE AXIS, NOW SPLIT IT ALONG ANOTHER
	#initialize multidimensional list to hold each dataframe, each value is first initialized to 0. Dimensions are num_binsXnum_bins
	longlat_list = [[0] * num_bins for i in range(num_bins)]

	#loop through each latitude slice and split each into longitude-defined squares.
	for l in range(num_bins):
		for x in range(num_bins):
			longlat_list[l][x] = lat_grid[l][(lat_grid[l][16] >= bin_bound[x][1]) & (lat_grid[l][16] < bin_bound[x+1][1])]
	return(longlat_list)

split_grid = grid(top_most,left_most,bottom_most,right_most,10)
create_geojson(split_grid[2][2])
print(split_grid[2][2])
print(len(split_grid))

#count the number in each bin

#define the color scale and how much to add to a given color based on number of trees

#give a color attribute to each bin, with intensity of color dependent on number of trees



# plt.show()



