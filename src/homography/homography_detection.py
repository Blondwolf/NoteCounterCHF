import cv2
import numpy as np
from matplotlib import pyplot as plt

from banknote import *

MIN_MATCH_COUNT = 38
FLANN_INDEX_KDTREE = 0

index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

sift = cv2.xfeatures2d.SIFT_create()
flann = cv2.FlannBasedMatcher(index_params, search_params)

des1 = None
des2 = None

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


def compute_homography(image, template_path, callback, current_note, list_notes, debug=False):
    points_list = []
    #img_final = cv2.imread(image_path, 1)
    img_final = image                     # Displayed image

    img1 = cv2.imread(template_path, 0)   # Matching templates
    img2 = img_final.copy()               # Image to compute

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)

    ended = False

    while not ended:
        points = find_match(img1, kp1, des1, img2, debug)

        if points is not None:
            points_list.append(points)              # Memorise points for other external usages
            img2 = cv2.fillPoly(img2, points, 255)  # Fill to mask and compute next search with same template
            callback(points, current_note, list_notes, img_final)                        # Main callback to notify found and return points

        else:
            ended = True

    return points_list #img_final

# Fouded callback from homography
def callback_founded(points, current_note, list_notes, image_final):
    # Draw Contour on image
    image_final = cv2.polylines(image_final, points, True, 255, 3, cv2.LINE_AA)  # Contour
    cv2.imshow("Homography", image_final)
    cv2.waitKey(1)

    # Note program
    list_notes.append(current_note)
    print("->Founded a " + str(current_note.value) + " note.")

def homography(image, debug=False):
    list_notes = []

    for color, note in NOTE_COLORS.items():
        for image_note_path in note.sides:
            current_note = note
            compute_homography(image, image_note_path, callback_founded, current_note, list_notes, debug)

    # Show note count
    print("The image show a sum of : " + str(sum(note.value for note in list_notes)))

    cv2.waitKey(0)