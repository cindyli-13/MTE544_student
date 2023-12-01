
from mapUtilities import *
from a_star import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
POINT_PLANNER=0; TRAJECTORY_PLANNER=1

class planner:
    def __init__(self, type_, mapName="room"):

        self.type=type_
        self.mapName=mapName

    
    def plan(self, startPose, endPose):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(endPose)
        
        elif self.type==TRAJECTORY_PLANNER:
            self.costMap=None
            self.initTrajectoryPlanner()
            return self.trajectory_planner(startPose, endPose)


    def point_planner(self, endPose):
        return endPose

    def initTrajectoryPlanner(self):


        # TODO PART 5 Create the cost-map, the laser_sig is 
        # the standard deviation for the gausiian for which
        # the mean is located on the occupant grid. 
        self.m_utilites=mapManipulator(laser_sig=0.3)
            
        self.costMap=self.m_utilites.make_likelihood_field()
        

    def trajectory_planner(self, startPoseCart, endPoseCart):


        # This is to convert the cartesian coordinates into the 
        # the pixel coordinates of the map image, remmember,
        # the cost-map is in pixels. You can by the way, convert the pixels
        # to the cartesian coordinates and work by that index, the a_star finds
        # the path regardless. 
        startPose=self.m_utilites.position_2_cell(startPoseCart)
        endPose=self.m_utilites.position_2_cell(endPoseCart)
        
        # TODO PART 5 convert the cell pixels into the cartesian coordinates
        path_cell = search(self.costMap, startPose, endPose, "euclidean")
        path_cart = list(map(self.m_utilites.cell_2_position, path_cell))

        obstacles = self.m_utilites.getAllObstacles()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        np.savetxt('obstaclesMap_' + formatted_datetime + '.txt', obstacles)
        np.savetxt('path_cart_' + formatted_datetime + '.txt', path_cart)
        np.savetxt('path_cell_' + formatted_datetime + '.txt', path_cell)
        np.savetxt('imageArray.txt', self.m_utilites.getMap())
        # TODO PART 5 return the path as list of [x,y]
        return path_cart




if __name__=="__main__":

    rclpy.init()

    m_utilites=mapManipulator()
    map_likelihood=m_utilites.make_likelihood_field()
    path=search(map_likelihood, (2,10), (70,90), 'euclidean') # changed 0 to [0,0]
    pathCart = list(map(m_utilites.cell_2_position, path))
    # obstacles = m_utilites.getAllObstacles()
    # plt.scatter([lin[0] for lin in obstacles], [lin[1] for lin in obstacles])
    imageArray = m_utilites.getMap()
    plt.imshow(imageArray, cmap='gray')
    plt.plot([lin[0] for lin in path], [lin[1] for lin in path])
    plt.show()