""" Gaussian Blur """
# Copyright (c) 2020. Mirage Technologies AG and its affiliates.
# All Rights Reserved

import warnings

import numpy as np
from boris import is_opencv_available

if is_opencv_available():
    import cv2
else:
    msg = 'cv2 is not available. Will skip Gaussian Blur augmentations.'
    warnings.warn(msg)


class GaussianBlur(object):
    # Implements Gaussian blur as described in the SimCLR paper
    def __init__(self, kernel_size, min=0.1, max=2.0, prob=0.5):
        self.min = min
        self.max = max
        self.prob = prob
        # kernel size is set to be 10% of the image height/width
        self.kernel_size = kernel_size
        if self.kernel_size % 2 == 0:
            self.kernel_size += 1

    def __call__(self, sample):
        sample = np.array(sample)

        if not is_opencv_available():
            return sample

        # blur the image with a 50% chance
        prob = np.random.random_sample()
        if prob < self.prob:
            sigma = (self.max - self.min) * \
                np.random.random_sample() + self.min

            sample = cv2.GaussianBlur(sample,
                                      (self.kernel_size, self.kernel_size),
                                      sigma)

        return sample
