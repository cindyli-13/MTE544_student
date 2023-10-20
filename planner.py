# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1
from math import exp, cos, sin, pi  
import numpy as np



def quadratic(x):
    return x**2

def sigma(x):
    return -1/(1+exp(-4*x))

def rotateByHeading(trajectory, heading):
    for point in trajectory:
        x = point[0]
        y = point[1]
        point[0] = cos(heading)*x - sin(heading)*y
        point[1] = sin(heading)*x + cos(heading)*y
    return trajectory


class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0, 0.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        theta = goalPoint[2]
        return x, y, theta

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        # parabola trajectory
        # dx = 0.1
        # tStart = -1
        # tEnd = 1
        # startingX = -1.389
        # startingY = -0.044
        # trajectory = [[quadratic(i), i] for i in np.arange(tEnd, tStart-dx, -dx)]
        # x = []
        # # trajectory = rotateByHeading(trajectory, -90*pi/180)
        
        # for i in range(len(trajectory)):
        #     if i == 0:
        #         x.append([startingX, startingY])
        #     else:
        #         stepX = trajectory[i][0]-trajectory[i-1][0]
        #         stepY = trajectory[i][1]-trajectory[i-1][1]
        #         x.append([x[i-1][0]+stepX, x[i-1][1]+stepY])

        # other thing trajectory
        dx = 0.1
        tStart = -1
        tEnd = 1
        startingX = -3.6
        startingY = -1.9
        trajectory = [[sigma(i), i] for i in np.arange(tEnd, tStart-dx, -dx)]
        x = []
        print(trajectory)
        # trajectory = rotateByHeading(trajectory, -90*pi/180)
        for i in range(len(trajectory)):
            if i == 0:
                x.append([startingX, startingY])
            else:
                stepX = trajectory[i][0]-trajectory[i-1][0]
                stepY = trajectory[i][1]-trajectory[i-1][1]
                x.append([x[i-1][0]+stepX, x[i-1][1]+stepY])
        # print(x)
        return x
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        # return 

