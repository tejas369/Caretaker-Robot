#import Libraries 
import numpy as np
import cv2
import collections
import heapq

class Graph:                                             #Class For Reading The Grid And Finding Obstacles And Edges 
                                                      
   def __init__(self):
      self.edges = {}
   
   def neighbours(self, id):                             #Finding The Neighbour Cells
      return self.edges[id]

class SquareMaze:                                        #Class For Traversing Through The Grid
   
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.weights = {}
    
    def value(self, a, b):                         
        return self.weights.get(b, 1)
      
    def in_bounds(self, id):                             #Checking Whether The Cell Lies Within The Boundary Limits Of The Grid 
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):                              #Checking Whether The Cell Is Obstacle Or Not 
        return id not in self.obstacles
    
    def neighbours(self, id):                            #Checking For Every Neighbour For Boundary Conditiions And Obstacles 
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() 
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


def trace_back(visited, start, goal):                    #Tracing The Shortest Traversed Path
    current = goal
    path = [current]
    while current != start:
        current = visited[current]
        path.append(current)
    return path


class PriorityQueue:                                     #Prioritizing And Adding The Elements To The Queue
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]



def heuristic(a, b):                                     #Calculation Of Manhattan Distance For A* Search 
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):                   #Function Of A* Alogrithm For Searching The Shortest Path 
    frontier = PriorityQueue()                           #Creating Priority Queue For Adding The Boundary Cells
    frontier.put(start, 0)                               #A Frontier Boundary For Searching Cells 
    visited = {}                                         #Dictionary Structure For Checking The Visited Or traversed Cells
    value_store = {}                                     #Dictionary Structure For Storing The Values Required For Moving To The Neighbour Cells 
    visited[start] = None                                   
    value_store[start] = 0                               #Intial Cell Has A Zero Value 
    
    while not frontier.empty():                          # Checking If The Queue For Boundary Cells Is Empty
        current = frontier.get()
        
        if current == goal:                              # Checking If The Goal Is Achieved
            break
        
        for next in graph.neighbours(current):           #Calculating The Values For Neighbour Cells For Setting The Priority Of Cells To Approach The Goal
            new_value = value_store[current] + graph.value(current, next)
            if next not in value_store or new_value < value_store[next]:
                value_store[next] = new_value
                priority = new_value + heuristic(goal, next)
                frontier.put(next, priority)
                visited[next] = current
    
    return visited, value_store                           # Returning The Values For Tracing Back The Path        

def play(img):                                     
    h,w,c = img.shape                                     # Obtainig The Dimensions Of The Image        
    grid =[]                                              # Creating List For Storing Coordinates Of Obstacles
    for i in range(1,11):                                 # Traversing Through The Grid                              
        for j in range(1,11): 
            cell = img[(i-1)*h/10:i*h/10,(j-1)*w/10:j*w/10,:]  #Seperating Individual Cells 
            avg = cv2.mean(cell)                          #Finding The Mean Value Of The Pixels  
            if (avg[0]>65 and avg[0]<66):                 #Comparing The Mean Value For Blue Color I.E Goal Cell
                    e1 = j                                #Storing The Coordinates Of The Goal Cell In (X(From Top Left To Right),Y(From Top To Bottom)) Format  
                    e2 = i
            if (avg[0]>174 and avg[0]<175 ):              #Comparing The Mean Value For Blue Color I.E Starting Cell  
                    s1 = j                                #Storing The Coordinates Of The Starting Cell In (X(From Top Left To Right),Y(From Top To Bottom)) Format
                    s2 = i
            if avg[0]<65:                                 #Comparing The Mean Value For Obstacle Such That Black[0](Obstacles)<Blue[65-66](Goal Cell)<Green[174-175](Starting Cell)                          
                grid.append((j,i))                        #List Of Obstacles                        
    g = SquareMaze(10, 10)                                #Passihg The Width And Height. g Is Object Of Class SquareMaze  
    g.obstacles = grid                                    #Storing The List Of Obstacles  
    start =(s1,s2)                                        #Tuple For Starting Coordinates  
    goal = (e1,e2)                                        #Tuple For Goal Coordinates  
    a,b = a_star_search(g,start,goal)                     #Calling The Function For Getting The Shortest Path And Obtaining The Visited And Values
    route_path = trace_back(a,start,goal)                 #Tracing Back The Path Including The Starting And Goal
    del route_path[0]                                     #Excluding The Starting Node  
    route_length = len(route_path)                        #Finding The Length Of The Shortest Path    
    return route_length, route_path


if __name__ == "__main__":
    #code for checking output for single image
    img = cv2.imread('test_images/test_image1.png')
    route_length, route_path = play(img)
    print "route length = ", route_length
    print "route path   = ", route_path
    #code for checking output for all images
    route_length_list = []
    route_path_list   = []
    for file_number in range(1,6):
        file_name = "test_images/test_image"+str(file_number)+".png"
        pic = cv2.imread(file_name)
        route_length, route_path = play(pic)
        route_length_list.append(route_length)
        route_path_list.append(route_path)
    print route_length_list
    print route_path_list
