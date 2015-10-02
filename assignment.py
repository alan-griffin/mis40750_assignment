import sqlite3
from math import *
import numpy as np


plant_location = []
port_location = []
port_to_plant = np.empty((10, 3), dtype=object)
plant_to_plant = np.empty((10, 10), dtype=object)
plant_info = np.empty((10, 4), dtype=object)
total_cost = np.empty((10, 2), dtype=object)

def plant_to_port_dist():
    index = 0
    for i in plant_location:
        port_dist(i[0], i[1], index) ; index += 1

def plant_to_plant_dist():
    index = 0
    for i in plant_location:
        plant_dist(i[0], i[1], index) ; index += 1

def port_dist(a, b, index):
    count = 0    
    for i in port_location:
        port_to_plant[index][count] = haversine(a,b,i[0],i[1])
        count += 1
        if count == 3: count = 0 ;
        
def plant_dist(a, b, index):
    count = 0    
    for i in plant_location:
        plant_to_plant[index][count] = haversine(a,b,i[0],i[1])
        count += 1
        if count == 10: count = 0 ;         
        
# Used haversine function to find distance between two points on earth
# Reference: https://en.wikipedia.org/wiki/Haversine_formula        
def haversine(a,b,c,d):
    e = b - d
    e = (1 - cos(e)) / 2      
    f = a - c           
    f = (1 - cos(f)) / 2 
    h = e + ((cos(b) * cos(d)) * f)     
    r = 6371    
    dist = 2 * r * asin(sqrt(h))
    return dist

     
def travel_to_plant():
    index = 0
    for i in range(0, len(plant_to_plant[index])):             
        summed_dist(index) ; index += 1 ;
        
def summed_dist(index):
    plant_info[index][0] = 0 ; plant_info[index][1] = 0
    for i in range(0, len(plant_to_plant[index])):    
        plant_info[index][0] += plant_to_plant[index][i]
        if i != index:  
            plant_info[index][1] += plant_location[i][2]
        else: plant_info[index][2] = plant_location[index][2]    

     
def nearest_port():
    for i in range(0, len(plant_info)):
        near(i)
    total_to_transport()    
        
def near(index):
    plant_info[index][3] = port_to_plant[index][0]
    for i in range(1, len(port_to_plant[index])):
        if port_to_plant[index][i] < plant_info[index][3]:
            plant_info[index][3] = port_to_plant[index][i]
 
def total_to_transport():
    index = 0
    for i in plant_info:
        plant_info[index][2] = plant_info[index][1] + plant_info[index][2]
        index += 1

# Made under assumption it costs $1 to transport 1 ton
def total_travel_cost():
    for i in range(0, len(plant_info)):
        total_cost[i][0] = (plant_info[i][0] * plant_info[i][1]) + \
        (plant_info[i][2] * plant_info[i][3])
        total_cost[i][1] = i


def find_location():
    location = 0
    cost = total_cost[0][1]
    for i in range(1, len(total_cost)):
        if cost > total_cost[i][0]: location = i ;
    return location
        
        
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM location;") # execute a SQL command
for item in c:
    plant_location.append(item)
c.execute("SELECT * FROM ports;") # execute a SQL command
for item in c: 
    port_location.append(item)

plant_to_port_dist()
plant_to_plant_dist()
travel_to_plant()
nearest_port()
total_travel_cost()
prime_location = find_location()
print "The prime location to locate the plant is at raw material station:" , \
     prime_location