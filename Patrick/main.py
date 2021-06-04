import numpy as np
from matplotlib import pyplot as plt

from src.BaseShapes import Point, Line, ConnectedSet, BLC, ConnectedPolygon


def get_random_polygon_vertices(n):
    # src: https://stackoverflow.com/questions/45831084/creating-a-polygon-in-python
    
    # start by randomly generating the vertices
    x = np.random.uniform(0,1,n)
    y = np.random.uniform(0,1,n)
    
    # computer the 'center point' of the polygon
    center_point = [np.sum(x)/n, np.sum(y)/n]
    
    # angles formed by each vertice with the center point
    angles = np.arctan2(x-center_point[0],y-center_point[1])
    
    # sort tuples 
    sort_tups = sorted([(i,j,k) for i,j,k in zip(x,y,angles)], key = lambda t: t[2])
    
    # check for duplicates
    if len(sort_tups) != len(set(sort_tups)):
        raise Exception('two equal coordinates -- exiting')
        
    x,y,angles = zip(*sort_tups)
    x = list(x)
    y = list(y)
    angles = list(angles)
    
    # close the loop by connecting the first and last vertices
    x.append(x[0])
    y.append(y[0])
    angles.append(angles[0])
    
    # TODO: CALL FUNCTION TO CALCULATE PEAK POINT USING 'VERTICES' AND 'ANGLES'
    
    
    return (x,y,angles)
    
def generate_random_connected_polygon(n):
    
    x, y, angles  = get_random_polygon_vertices(n)
    
    # for now set peak point to be the mid point between adjacent vertices
    # TODO: add function to calculate peakPoint using curvature/angle
    points = []
    for i in range(len(x)-1):
        # start by appending current (x, y) point
        curr = Point(x[i], y[i])
        points.append(curr)
        
        # calculate mid-point between current and next, and append it
        next = Point(x[i+1], y[i+1])
        mid = curr.midpointTo(next)
        points.append(mid)
    
    # append last (x, y) points
    last = Point(x[-1], y[-1])
    points.append(last)
    
    # create ConnectedPolygon object and return it
    number_of_vertices = n * 2 + 1
    return ConnectedPolygon(points, number_of_vertices)
    
# TODO: randomly generate BLCs (dis-connected polygons) 


# TEST BY GENERATING 20 TRIANGLES / SQUARES / HEXAGONS
if __name__ == '__main__':
    triangles = []
    fig,ax = plt.subplots()
    for i in range(20):
        triangle = generate_random_connected_polygon(3)
        triangle.draw(ax)
        triangles.append(triangle)
    
    #print(triangles)
    plt.show()