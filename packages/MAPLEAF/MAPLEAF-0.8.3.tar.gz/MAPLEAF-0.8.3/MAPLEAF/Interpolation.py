'''
Linear interpolation on sorted lists of values and rigid body states
'''
from bisect import bisect

import numpy as np

from MAPLEAF.Motion.RigidBodyStates import RigidBodyState, RigidBodyState_3DoF


def linInterp(X, Y, desiredX):
    '''
        Arguments:
            X: Sorted list or numpy array of numeric x-values
            Y: Sorted list or numpy array of numeric y-values
            desiredX: Numeric x-value, indicating point to interpolate to

        Returns:
            desiredY: The linearly-interpolated y value at x=desiredX

        Notes:
            Uses binary search (bisect) to locate interpolation interval
            Faster than built-in methods for our application (see test/LinInterpSpeed.py)
    '''
    interpPt = bisect(X, desiredX)
    
    if interpPt >= len(X):
        return Y[len(X)-1]
    elif interpPt < 1:
        return Y[0]
    else:
        lgX = X[interpPt]
        smX = X[interpPt-1]
        lgY = Y[interpPt]
        smY = Y[interpPt-1]

    return (lgY - smY)*(desiredX - smX)/(lgX - smX) + smY

def linInterpWeights(X, desiredX):
    ''' 
        Expects the list X is sorted
        Returns smallYIndex, smallYWeight, largeYIndex, largeYWeight:
            Ex: X = [ 0, 1, 2, 3 ], desiredX = 0.75
                smallYIndex = 0
                smallYWeight = 0.25
                largeYIndex = 1
                largeYWeight = 0.75

            Then, to calculate the interpolate value:
                interpVal = Y[smallYIndex]*smallYWeight + Y[largeYIndex]*largeYWeight
    '''
    interpPt = bisect(X, desiredX)

    #Edge cases
    if interpPt >= len(X):
        return 0, 0, -1, 1
    elif interpPt < 1:
        return 0, 1, 0, 0

    # Normal cases
    smallYIndex = interpPt -1
    largeYIndex = interpPt
    largeYWeight = (desiredX - X[smallYIndex]) / (X[largeYIndex] - X[smallYIndex])
    smallYWeight = 1 - largeYWeight

    return smallYIndex, smallYWeight, largeYIndex, largeYWeight
    
def calculateCubicInterpCoefficients(X1, X2, Y1, Y2, dydx1, dydx2):
    ''' Returns coefficients for a cubic polynomial that matches values and derivatives at x1 and x2 '''
    # AMatrix and B, together define the following equations which constrain the cubic interpolation
    # f(x=x1)       == Y1
    # f(x=x2)       == Y2
    # df/dx (x=x1)  == dydx1
    # df/dx (x=x2)  == dydx2
    AMatrix = \
        np.array([  [ 1,    X1, X1**2,  X1**3 ],
                    [ 1,    X2, X2**2,  X2**3 ],
                    [ 0,    1,  2*X1, 3*X1**2 ],
                    [ 0,    1,  2*X2, 3*X2**2 ] ])
    
    B = np.array([  [Y1], 
                    [Y2], 
                    [dydx1], 
                    [dydx2]])

    return np.linalg.inv(AMatrix).dot(B)

def cubicInterp(X, X1, X2, Y1, Y2, Y1_plusDx, Y2_plusDx, dx):
    dy_dx_x1 = (Y1_plusDx - Y1) / dx
    dy_dx_x2 = (Y2_plusDx - Y2) / dx

    interpCoeffs = calculateCubicInterpCoefficients(X1, X2, Y1, Y2, dy_dx_x1, dy_dx_x2)
    return float(interpCoeffs[0] + interpCoeffs[1]*X + interpCoeffs[2]*X**2 + interpCoeffs[3]*X**3)

def interpolateRigidBodyStates(state1, state2, state1Weight):
    '''
        Linearly interpolates between state 1 and state2.
        state1Weight should be a decimal value between 0 and 1.
    '''
    state2Weight = 1 - state1Weight
    
    # Properties of all rigid body states
    pos = state1.position*state1Weight + state2.position*state2Weight
    vel = state1.velocity*state1Weight + state2.velocity*state2Weight

    try:
        # 6DoF Properties
        orientationDelta = state1.orientation.slerp(state2.orientation, state1Weight) # Use spherical linear interpolation for quaternions
        orientation = state1.orientation * orientationDelta
        angVel = state1.angularVelocity*state1Weight + state2.angularVelocity*state2Weight
        return RigidBodyState(pos, vel, orientation, angVel)

    except AttributeError:
        # 3DoF doesn't include orientation / angVel
        return RigidBodyState_3DoF(pos, vel)
