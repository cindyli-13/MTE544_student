

import numpy as np



# TODO Part 3: Comment the code explaining each part
class kalman_filter:
    '''
    This is an implementation of the Extended Kalman Filter (EKF) for the TurtleBot4 to perform state estimation
    using IMU and odometry measurements.
    '''
    
    # TODO Part 3: Initialize the covariances and the states    
    def __init__(self, P,Q,R, x, dt):
        
        self.P = P      # covariance matrix of state errors
        self.Q = Q      # covariance matrix of process noise
        self.R = R      # covariance matrix of measurement noise
        self.x = x      # state vector
        self.dt = dt    # filter update time step (assumed to be constant in our case)
        
    # TODO Part 3: Replace the matrices with Jacobians where needed        
    def predict(self):
        '''
        The first step of the EKF is the predict step. We predict our new state using our motion model.
        We also propagate our state errors covariance matrix (P) based on our motion model and process noise.
        '''
        
        self.A = self.jacobian_A()   # matrix A is the state transition matrix from x[k] to x[k+1]
                                     # as part of the EKF, we obtain A by linearizing our non-linear motion 
                                     # model at each time step by taking its Jacobian matrix
        self.C = self.jacobian_H()   # matrix C is the state-to-measurement conversion matrix
                                     # as part of the EKF, we obtain C by linearizing our non-linear measurement
                                     # model at each time step by taking its Jacobian matrix
        
        self.motion_model() # apply the motion model: x[k+1] = g(x[k])
                            # in our case, we do not model any control inputs u[k]
        
        self.P= np.dot( np.dot(self.A, self.P), self.A.T) + self.Q  # propagate state covariance matrix by applying 
                                                                    # linearized motion model and adding process noise
                                                                    # this matrix reflects the uncertainty in our state
                                                                    # due to errors in the prediction step

    # TODO Part 3: Replace the matrices with Jacobians where needed
    def update(self, z):
        '''
        The second step of the EKF is the update step. We correct our predicted state based on our sensor measurements.
        The degree to which we trust our sensor measurements is captured in the Kalman gain (K), which is recomputed at
        each time step. We also correct our state errors covariance matrix (P) using the Kalman gain.
        '''
        
        S=np.dot(np.dot(self.C, self.P), self.C.T) + self.R     # compute intermediate variable S by applying measurement model 
                                                                # to P and adding measurement noise
            
        kalman_gain=np.dot(np.dot(self.P, self.C.T), np.linalg.inv(S))  # compute Kalman gain
        
        surprise_error= z - self.measurement_model()    # compute innovation (aka the discrepancy between our predicted state 
                                                        # and what our sensors actually measured)
        
        self.x=self.x + np.dot(kalman_gain, surprise_error)     # correct our state with the Kalman gain and innovation
        self.P=np.dot( (np.eye(self.A.shape[0]) - np.dot(kalman_gain, self.C)) , self.P)    # correct our state covariance matrix with
                                                                                            # the Kalman gain and measurement model
        
    
    # TODO Part 3: Implement here the measurement model
    def measurement_model(self):
        '''
        The measurement model computes the expected measurement vector given the state vector: z[k] = h(x[k])
        '''
        x, y, th, w, v, vdot = self.x
        return np.array([
            v,# v
            w,# w
            vdot, # ax
            v*w, # ay
        ])
        
    # TODO Part 3: Impelment the motion model (state-transition matrice)
    def motion_model(self):
        '''
        The motion model computes the new state given the current state: x[k+1] = g(x[k]).
        In our case it is based on the kinematics of a 2WD robot.
        '''
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        self.x = np.array([
            x + v * np.cos(th) * dt,
            y + v * np.sin(th) * dt,
            th + w * dt,
            w,
            v  + vdot*dt,
            vdot,
        ])
        


    
    def jacobian_A(self):
        '''
        Computes the Jacobian of the motion model g(x).
        '''
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        return np.array([
            #x, y,      th,              w,          v,              vdot
            [1, 0,     -v*np.sin(th)*dt, 0,          np.cos(th)*dt,  0],
            [0, 1,      v*np.cos(th)*dt, 0,          np.sin(th)*dt,  0],
            [0, 0,      1,               dt,         0,              0],
            [0, 0,      0,               1,          0,              0],
            [0, 0,      0,               0,          1,              dt],
            [0, 0,      0,               0,          0,              1 ]
        ])
    
    
    # TODO Part 3: Implement here the jacobian of the H matrix (measurements)    
    def jacobian_H(self):
        '''
        Computes the Jacobian of the measurement model h(x).
        '''
        x, y, th, w, v, vdot=self.x
        return np.array([
            #x, y,th, w, v,vdot
            [0,0,0  , 0, 1, 0], # v
            [0,0,0  , 1, 0, 0], # w
            [0,0,0  , 0, 0, 1], # ax
            [0,0,0  , v, w, 0], # ay
        ])
        
    # TODO Part 3: return the states here    
    def get_states(self):
        return self.x
