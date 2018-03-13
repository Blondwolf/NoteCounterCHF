import cv2
import numpy as np
from matplotlib import pyplot as plt

from .banknote import *

MIN_MATCH_COUNT = 40
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

sift = cv2.xfeatures2d.SIFT_create()
flann = cv2.FlannBasedMatcher(index_params, search_params)

def find_match(img1, kp1, des1, img2, debug=False):
    points = None

    kp2, des2 = sift.detectAndCompute(img2, None)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0) #cv2.LMED
        matchesMask = mask.ravel().tolist()

        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        points = [np.int32(dst)]

        print("Founded match - %d/%d similarities" % (len(good), MIN_MATCH_COUNT))

        if debug:
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)  # Lines

            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)

            img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
            plt.imshow(img3, 'gray'), plt.show()

    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))

    return points


def homography(self, image):
    pass