from typing import final
from geopy.geocoders import Nominatim
from geopy import distance
import numpy as np
import time, itertools
import random
from .models import distanceModel
start = time.time()

def getDistance(source, dest):
    try:
        dbDistance1 = distanceModel.objects.get(source=dest, dest=source)
    except:
        dbDistance1 = None
    try:
        dbDistance2 = distanceModel.objects.get(source=dest, dest=source)
    except:
        dbDistance2 = None
    if dbDistance2!=None:
        # print("distance found", dbDistance1.source, dbDistance1.dest, dbDistance1.distance)
        return int(dbDistance2.distance)
    if dbDistance1!=None:
        # print("distance found", dbDistance2.source, dbDistance2.dest, dbDistance2.distance)
        return int(dbDistance1.distance)
    try:
        geocoder = Nominatim(user_agent="Sarvesh")

        coordinates1 = geocoder.geocode(source)
        coordinates2 = geocoder.geocode(dest)
        print(source, coordinates1)
        print(dest, coordinates2)
        place1 = (coordinates1.latitude, coordinates1.longitude)
        place2 = (coordinates2.latitude, coordinates2.longitude)
        print("distance finding", source, " to ",dest)

        saver = distanceModel.objects.create(source=source, dest=dest, distance=int(distance.distance(place1, place2).km))
        saver.save()
        saver = distanceModel.objects.create(source=dest, dest=source, distance=int(distance.distance(place1, place2).km))
        saver.save()
        return int(distance.distance(place1, place2).km)
    except Exception as e:
        print(e)
    return 0

def getDistanceByList(locList):
    
    Map = {}
    for i in range(len(locList)):
        src=locList[i]
        Map[src] = {}
    for subset in itertools.combinations(locList, 2):
            src, dest = subset
            distanceBetweenLocations = getDistance(src, dest)
            # distanceBetweenLocations = random.randint(0, 10)
            
            Map[src][dest] = distanceBetweenLocations
            Map[dest][src] = distanceBetweenLocations
    return Map

def createGraph(Map, locList):
    graph = []
    
    for i in range(len(locList)):
        graph.append([])
        for j in range(len(locList)):
            graph[i].append(0)
            if i == j:
                graph[i][j] = 0
            else:
                graph[i][j] = Map[locList[i]][locList[j]]
                
    return graph
# Python3 implementation of the approach
# Function to find the minimum weight
# Hamiltonian Cycle
def tsp(graph, v, currPos, n, count, cost, strans, locList, answerArray, answer):

	# If last node is reached and it has
	# a link to the starting node i.e
	# the source then keep the minimum
	# value out of the total cost of
	# traversal and "ans"
	# Finally return to check for
	# more possible values
	if (count == n and graph[currPos][0]):
        
		answer.append(cost + graph[currPos][0]); answerArray.append(strans)
		return

	# BACKTRACKING STEP
	# Loop to traverse the adjacency list
	# of currPos node and increasing the count
	# by 1 and cost by graph[currPos][i] value
	for i in range(n):
		if (v[i] == False and graph[currPos][i]):
			
			# Mark as visited
			v[i] = True
			tsp(graph, v, i, n, count + 1, cost + graph[currPos][i], strans + ", " + locList[i], locList, answerArray, answer)
			
			# Mark ith node as unvisited
			v[i] = False

def getPath(locList):
    Map = getDistanceByList(locList)
    graph = createGraph(Map, locList)
    n = len(locList)
    answer = []
    v = [False for i in range(n)]

    # Mark 0th node as visited
    v[0] = True
    answerArray = []
    # Find the minimum weight Hamiltonian Cycle
    tsp(graph, v, 0, n, 1, 0, locList[0] + "", locList, answerArray, answer)

    # ans is the minimum weight Hamiltonian Cycle
    finalPath = answerArray[answer.index(min(answer))] + ", " + locList[0]
    return finalPath, min(answer), Map

if __name__ == "__main__":
    start = time.time()
    locList = ["Bhopal", "pachmarhi", "Leh", "Achalpur"]
    
    np.random.shuffle(locList)
    path, minDistance, Map = getPath(locList)
    print("total time taken", time.time() - start)
    print(path.split())
    print(minDistance)
    print(Map)

