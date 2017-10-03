
from __future__ import division

import cv2
import numpy as np
from scipy.signal import fftconvolve

from .GaborKernel import gaborkernel
from Tools.Float2Uint import float2Uint
from Tools.Standardize import globalstandardize

def gaborFiltering(Img_green_reverse, Mask):

    height, width = Img_green_reverse.shape

    psi = [0, np.pi/2]
    gamma = 1
    bandwidth = 1
    rotationNumber = 10
    lambdas = np.arange(1, 11, 2)

    filteredImg_scales = np.zeros((height, width, len(lambdas)))
    for index, lambda0 in enumerate(lambdas):
        # print(lambda0)
        gaborFilteredImage = gaborFilteringSubLoop(Img_green_reverse, Mask, lambda0, psi, gamma, bandwidth, rotationNumber)
        filteredImg_scales[:,:,index] = gaborFilteredImage


    filteredImg1 = np.amax(filteredImg_scales, axis = 2)
    filteredImg1 = float2Uint(filteredImg1)

    filteredImg2 = np.mean(filteredImg_scales, axis = 2)
    filteredImg2 = float2Uint(filteredImg2)

    return filteredImg1, filteredImg2


def gaborFilteringSubLoop(Img_green_reverse, Mask, lambda0, psi, gamma, bandwidth, rotationNumber):


    gaborFilteredImage_rotations = np.zeros((Img_green_reverse.shape[0], Img_green_reverse.shape[1], rotationNumber))
    for n in xrange(0, rotationNumber):
        theta = n * np.pi / rotationNumber
        gkernel = gaborkernel(bandwidth, gamma, psi[0], lambda0, theta)
        gaborFilteredImage_rotations[:, :, n] = fftconvolve(Img_green_reverse, gkernel, mode='same')

    gaborFilteredImage = np.max(gaborFilteredImage_rotations, axis=2)
    gaborFilteredImage = globalstandardize(gaborFilteredImage, Mask)
    gaborFilteredImage[gaborFilteredImage < 0] = 0
    gaborFilteredImage = gaborFilteredImage / np.max(gaborFilteredImage)

    return gaborFilteredImage


# ###################
# from multiprocessing import Pool
# def gaborFiltering_multiprocessing(Img_green_reverse, Mask):
#
#     height, width = Img_green_reverse.shape
#
#     psi = [0, np.pi/2]
#     gamma = 1
#     bandwidth = 1
#     rotationNumber = 10
#     lambdas = np.arange(1, 11, 2)
#
#     p = Pool()
#     pool_parameters = []
#
#     filteredImg_scales = np.zeros((height, width, len(lambdas)))
#     for index, lambda0 in enumerate(lambdas):
#         pool_parameters.append((Img_green_reverse, Mask, lambda0, psi, gamma, bandwidth, rotationNumber))
#
#     gaborFilteredImage_array = p.map(gaborFilteringSubLoop, pool_parameters)
#     for index, _ in enumerate(lambdas):
#         filteredImg_scales[:, :, index] = gaborFilteredImage_array[index]
#
#     filteredImg1 = np.amax(filteredImg_scales, axis = 2)
#     filteredImg1 = float2Uint(filteredImg1)
#
#     filteredImg2 = np.mean(filteredImg_scales, axis = 2)
#     filteredImg2 = float2Uint(filteredImg2)
#
#     return filteredImg1, filteredImg2
