# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1
# Type of trajectory 
QUADRATIC=0; SIGMOID=1
from math import exp, cos, sin, pi  
import numpy as np

# calculate the quadratic equation
def quadratic(x):
    return x**2

# calculate the sigmoid function. Note that the exponent scalar was increased to make the motion more drastic for demo. 
def sigmoid(x):
    return -1/(1+exp(-4*x))

# rotate the trajectory by a specified heading in radians, was not used for lab. 
def rotateByHeading(trajectory, heading):
    for point in trajectory:
        x = point[0]
        y = point[1]
        point[0] = cos(heading)*x - sin(heading)*y
        point[1] = sin(heading)*x + cos(heading)*y
    return trajectory


class planner:
    def __init__(self, type_, trajectoryType=QUADRATIC):

        self.type=type_ # motion type
        self.trajectoryType = trajectoryType # trajectory type

    
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
    
        if self.trajectoryType==QUADRATIC:
            
            dx = 0.1
            tStart = -1 # start independent variable value of the parabola
            tEnd = 1 # end independent variable value of the parabola

            # robot's starting pose
            startingX = -1.389
            startingY = -0.044

            # calculate the dependent variable, notice it is flipped with y as independent and x as dependent
            # this was done to make the motion work in the lab.
            # notice the end and start is flipped. this is also to make the motion work on the lab floor
            trajectory = [[quadratic(i), i] for i in np.arange(tEnd, tStart-dx, -dx)]
            x = []

            for i in range(len(trajectory)):
                # make the first point of the trajectory its own starting pose.
                if i == 0:
                    x.append([startingX, startingY])
                else:
                    # find the difference between two trajectory points and add this to the previous x,y values to form
                    # the points required for the robot to trace this motion starting from its own starting point. 
                    stepX = trajectory[i][0]-trajectory[i-1][0]
                    stepY = trajectory[i][1]-trajectory[i-1][1]
                    x.append([x[i-1][0]+stepX, x[i-1][1]+stepY])

        # the logic here is the same as above except the function is different. 
        elif self.trajectoryType==SIGMOID:
            dx = 0.1
            tStart = -1
            tEnd = 1
            startingX = -3.6
            startingY = -1.9
            trajectory = [[sigmoid(i), i] for i in np.arange(tEnd, tStart-dx, -dx)]
            x = []
            for i in range(len(trajectory)):
                if i == 0:
                    x.append([startingX, startingY])
                else:
                    stepX = trajectory[i][0]-trajectory[i-1][0]
                    stepY = trajectory[i][1]-trajectory[i-1][1]
                    x.append([x[i-1][0]+stepX, x[i-1][1]+stepY])
        else:
            x = []
            print("No such trajectory type")
        return x

