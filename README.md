# MIS40750 Assignment
### Alan Griffin - 11535803

###### Goal: To find location for new processing plant given coordinates for several raw material locations and nearby ports

Assumptions Made:
- Whichever location is selected for plant, this location will still
  produce raw materials
- Arbitrary cost of $1 per km chosen as price to transport one ton of raw
  material 
- Plant locations are numbered 0-9, in the order they are read in
- Port locations are numbered 0-2, under same assumption

Solution steps:
- Data is read from the database into two lists, one for plant information and the other for port information
- The distance from each potential plant to all ports is calculated, using the haversine function
- The distance from each potential plant to all other possible plants is calculated, again using the haversine function
- For each possible plant, the total distance to all other sites is calculated, plus the amount of raw material which would have to be transported to the new plant
- For each possible plant, the nearest port is found
- For each possible plant, the total weight of goods to be transported to the nearest port is calculated, which includes those produced at the new plant
- As such, the total travel cost is calculated. For each plant, under the assumption that it costs $1 to transport 1 ton per km, we calculate the cost of transporting all raw material from other locations to the plant and then the cost of transporting all material (including that produced at plant) to the port
- The location with the lowest total cost is selected along with its accompanying port

Program Output:
- The prime location to locate the plant is at raw material location 0 while shipping to port 2
- Raw material location 0 chosen for plant. Coordinates:
Latitude : 52.66
Longitude: 7.26
- Port 2 chosen. Coordinates:
Latitude : 52.27
Longitude: 6.39