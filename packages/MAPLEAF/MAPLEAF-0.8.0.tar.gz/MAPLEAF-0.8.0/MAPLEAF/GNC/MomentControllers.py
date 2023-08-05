import abc

import numpy as np

import MAPLEAF.Rocket.AeroFunctions as AeroFunctions
from MAPLEAF.GNC.PID import GainScheduledPIDController


class MomentController(abc.ABC):
    @abc.abstractmethod
    def getDesiredMoments(self, rocketState, environment, targetOrientation, time, dt):
        ''' Should return a list [ desired x-axis, y-axis, and z-axis ] moments '''

class GainScheduledPIDRocketMomentController(MomentController, GainScheduledPIDController):
    def __init__(self, gainTableFilePath, keyColumnNames):
        '''
            Assumes the longitudinal (Pitch/Yaw) PID coefficients are in columns nKeyColumns:nKeyColumns+2
            Assumes the roll PID coefficients are in columns nKeyColumns+3:nKeyColumns+5
            Sample gain file: test/test_GNC/testPIDCoeffs.txt
        '''
        self.keyFunctionList = [ AeroFunctions.stringToAeroFunctionMap[x] for x in keyColumnNames ]
        nKeyColumns = len(keyColumnNames)
        GainScheduledPIDController.__init__(self, gainTableFilePath, nKeyColumns, PCol=nKeyColumns, DCol=nKeyColumns+5)
        
    def updateCoefficientsFromGainTable(self, keyList):
        ''' Overriding parent class method to enable separate longitudinal and roll coefficients in a single controller '''
        Pxy, Ixy, Dxy, Pz, Iz, Dz = self._getPIDCoeffs(*keyList)

        # Coefficient for each of P, I, and D are: Longitudinal, Longitudinal, Roll
        # Operates the internal PID controller in vector-mode with numpy arrays (using their elementwise operations)
        P = np.array([Pxy, Pxy, Pz])
        I = np.array([Ixy, Ixy, Iz])
        D = np.array([Dxy, Dxy, Dz])
        self.updateCoefficients(P, I, D)

    def _getOrientationError(self, rocketState, targetOrientation):
        return np.array((targetOrientation / rocketState.orientation).toRotationVector())

    def getDesiredMoments(self, rocketState, environment, targetOrientation, time, dt):
        '''
            Inputs: 
                gainKeyList:        iterable of length nKeyColumns, containing the data required to interpolate the PIDxy and PIDz coefficients in the gain table
                rocketState:        must have .orientation attribute (Quaternion)
                targetOrientation:  (Quaternion)
                _:                  currently unused (time argument)
                dt:                 (numeric) time since last execution of the control system
        '''
        orientationError = self._getOrientationError(rocketState, targetOrientation)
        gainKeyList = AeroFunctions.getAeroPropertiesList(self.keyFunctionList, rocketState, environment)
        self.updateCoefficientsFromGainTable(gainKeyList)
        return self.getNewSetPoint(orientationError, dt)
