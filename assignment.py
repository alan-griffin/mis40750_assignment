# Alan Griffin - 11535803
# MIS40750 Assignment

import sqlite3
from math import asin, cos, sqrt
import numpy as np


plant_location = []
port_location = []
port_to_plant = np.empty((10, 3), dtype=object)
plant_to_plant = np.empty((10, 10), dtype=object)
plant_info = np.empty((10, 5), dtype=object)
total_cost = np.empty((10, 2), dtype=object)
location = np.empty((2), dtype=object)

# Assumptions
# - Whichever location selected for plant, this location will still
#   produce raw materials
# - Arbitrary cost of $1 per km chosen as price to transport one ton of raw
#   material 
# - Plant locations are numbered 0-9, in the order they are read in
# - Port locations are numbered 0-2, under same assumption

# Main function used to run program
def run():
    conn = sqlite3.connect('renewable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM location;") # Get plant data
    for item in c:
        plant_location.append(item)
    c.execute("SELECT * FROM ports;") # Get port data
    for item in c: 
        port_location.append(item)     
    
    plant_to_port_dist()
    plant_to_plant_dist()
    travel_to_plant()
    nearest_port()
    total_travel_cost()
    prime_location = find_location()
    
    print ""    
    print "The prime location to locate the plant is at raw material location",\
    prime_location[0], "while shipping to port", prime_location[1]
    
    print ""
    print "Raw material location", prime_location[0], "chosen for plant. " \
          "Coordinates:"
    print "Latitude :", plant_location[prime_location[0]][0]
    print "Longitude:", plant_location[prime_location[0]][1]
    
    print ""
    print "Port", prime_location[1], "chosen. Coordinates:"
    print "Latitude :", port_location[prime_location[1]][0]
    print "Longitude:", port_location[prime_location[1]][1]


# Set of functions which for each plant location, calculates 
#the distance to each of the ports, using port_dist and 
# haversine functions
def plant_to_port_dist():
    index = 0
    for i in plant_location:
        port_dist(i[0], i[1], index) ; index += 1

# Calculates the distance of the current plant, which is passed 
# to the function as a set of coordinates and an index value, to
# each of the ports. Haversine function used to compute distance.
def port_dist(a, b, index):
    count = 0    
    for i in port_location:
        port_to_plant[index][count] = haversine(a,b,i[0],i[1])
        count += 1


# Set of functions which for each plant, calculates the distance
# to all other plants  
def plant_to_plant_dist():
    index = 0
    for i in plant_location:
        plant_dist(i[0], i[1], index) ; index += 1
        
# Function which is passed plant coordinates and an index value as a
# parameter, and computes the distance of the current plant to all
# other plants     
def plant_dist(a, b, index):
    count = 0    
    for i in plant_location:
        plant_to_plant[index][count] = haversine(a,b,i[0],i[1])
        count += 1

        
# Used haversine function to find distance between two points on earth
# Reference: https://en.wikipedia.org/wiki/Haversine_formula        
def haversine(a,b,c,d):
    e = a - c
    e = (1 - cos(e)) / 2      
    f = b - d           
    f = (1 - cos(f)) / 2 
    h = e + ((cos(a) * cos(c)) * f)     
    r = 6371 # Radius of Earth    
    dist = 2 * r * asin(sqrt(h))
    return dist

     
def travel_to_plant():
    for index in range(0, len(plant_to_plant)):           
        plant_info[index][0] = 0 ; plant_info[index][1] = 0
        for i in range(0, len(plant_to_plant[index])):    
            # Calculates total distance of all other plants to current plant            
            plant_info[index][0] += plant_to_plant[index][i]
            # Calculates total weight of material which must be shipped to
            # current plant            
            if i != index:  
                plant_info[index][1] += plant_location[i][2]
            # Assigns amount of material created at current plant separately
            else: plant_info[index][2] = plant_location[index][2]       


# Function which for each plant, finds its nearest port     
def nearest_port():
    for index in range(0, len(plant_info)):
        plant_info[index][3] = port_to_plant[index][0]
        plant_info[index][4] = 0
        for i in range(1, len(port_to_plant[index])):
            if port_to_plant[index][i] < plant_info[index][3]:
                plant_info[index][3] = port_to_plant[index][i]
                plant_info[index][4] = i
    total_to_transport()    
 

# Function which calculates the total weight of goods to be transported
# from the plant to the port, if all raw material clustered in one location
# i.e. adds raw material from other locations to those created at the plant
def total_to_transport():
    index = 0
    for i in plant_info:
        plant_info[index][2] = plant_info[index][1] + plant_info[index][2]
        index += 1

# As such, the total travel cost is calculated. For each plant, under the
# assumption that it costs $1 to transport 1 ton per km, we calculate the cost
# of transporting all raw material from other locations to the plant and
# then the cost of transporting all material (including that produced at plant)
# to the port
def total_travel_cost():
    for i in range(0, len(plant_info)):
        total_cost[i][0] = (plant_info[i][0] * plant_info[i][1]) + \
        (plant_info[i][2] * plant_info[i][3])
        total_cost[i][1] = i

# Plant with the lowest total cost is selected along with its accompanying
# port  
def find_location():
    location[0] = 0 ; location[1] = plant_info[0][4]
    cost = total_cost[0][1]
    for i in range(1, len(total_cost)):
        if cost > total_cost[i][0]: 
            cost = total_cost[i][1]
            location[1] = plant_info[i][4]
            location[0] = i 
    return location
    
    
# Call to run program    
run()