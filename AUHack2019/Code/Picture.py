from MatrixCalculations import MatrixCalculations
import copy
import numpy as np

class ImageConcretion:
    def __init__(self):
        self.MC = MatrixCalculations()


    def make_snapshot_of_model(self, model):
        D2Matrix = model[0]
        CMatrix  = model[1]

        zeroMatrix = self.MC.generate_zero_matrix(200, 200)
        plusFactor = 100
        #Insert points
        for point in D2Matrix:
            zeroMatrix[int(point[0])+plusFactor][int(point[1])+plusFactor] = 1

        for rowCounter, connectionRow in enumerate(CMatrix):
            for counter, connection in enumerate(connectionRow):
                if connection == 1 and counter > rowCounter:
                    pointA = D2Matrix[rowCounter]
                    pointB = D2Matrix[counter]
                    pointC = copy.deepcopy(pointA)
                    toggleX = 0
                    toggleY = 0
                    [toggleX, toggleY] = self._calculate_diff_toggle(pointA, pointB, pointC)
                    toggleCounterX = 0
                    toggleCounterY = 0

                    while int(pointC[0]) != int(pointB[0]) or int(pointC[1]) != int(pointB[1]):
                        if toggleX <= toggleCounterX and toggleY <= toggleCounterY:
                            [toggleX, toggleY] = self._calculate_diff_toggle(pointC, pointB, pointC)
                            toggleCounterX = 0
                            toggleCounterY = 0

                        if toggleCounterX < toggleX:
                            toggleCounterX = toggleCounterX + 1
                            diff = int(pointB[0]) - int(pointC[0])
                            if diff > 0:
                                pointC[0] = int(pointC[0])+1
                                zeroMatrix[int(pointC[0]+plusFactor)][int(pointC[1]+plusFactor)] = 1
                            elif diff < 0:
                                pointC[0] = int(pointC[0])-1
                                zeroMatrix[int(pointC[0]+plusFactor)][int(pointC[1]+plusFactor)] = 1

                        if toggleCounterY < toggleY:
                            toggleCounterY = toggleCounterY + 1
                            diff = int(pointB[1]) - int(pointC[1])
                            if diff > 0:
                                pointC[1] = int(pointC[1])+1
                                zeroMatrix[int(pointC[0]+plusFactor)][int(pointC[1]+plusFactor)] = 1
                            elif diff < 0:
                                pointC[1] = int(pointC[1])-1
                                zeroMatrix[int(pointC[0]+plusFactor)][int(pointC[1]+plusFactor)] = 1

        return zeroMatrix


    def _calculate_diff_toggle(self, point_a, point_b, point_c):
        diff0 = float(int(point_b[0]) - int(point_c[0]))
        flagDiff0 = 0
        if diff0 < 0:
            diff0 = -diff0
        if(diff0 == 0):
            flagDiff0 = 1
            diff0 = 1

        diff1 = float(int(point_b[1]) - int(point_c[1]))
        flagDiff1 = 0
        if diff0 < 0:
            diff1 = -diff1
        if(diff1 == 0):
            flagDiff1 = 1
            diff1 = 1

        ratio = diff0/diff1

        if ratio < 0:
            ratio = -ratio

        if(ratio > 1):
            toggleX = 1*ratio
            toggleY = 1
            if flagDiff1 == 1:
                toggleY = 0
        else:
            toggleX = 1
            toggleY = 1/ratio
            if flagDiff0 == 1:
                toggleX = 0

        return [round(toggleX), round(toggleY)]


    def convert_snapshot_to_image(self, snapshot_array):
        img = np.zeros(shape=[200, 200, 3], dtype=np.uint8)

        for colCounter, col in enumerate(img):
            for elementCounter, colElement in enumerate(img):
                if snapshot_array[colCounter][elementCounter] == 0:
                    img[colCounter][elementCounter][0] = 255
                    img[colCounter][elementCounter][1] = 255
                    img[colCounter][elementCounter][2] = 255
                else:
                    img[colCounter][elementCounter][0] = 0
                    img[colCounter][elementCounter][1] = 0
                    img[colCounter][elementCounter][2] = 0
        return img
