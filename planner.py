# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1
from math import exp




def quadratic(x):
    return -x**2

def sigma(x):
    return -3/(1+exp(-3*x))


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
        dx = 0.5
        x = [[i*dx, sigma(i*dx)] for i in range(10)]
        print(x)
        return x
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        # return 

