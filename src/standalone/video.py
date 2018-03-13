import cv2

from banknote import note_colors
from standalone.homography import find_match

image_final = None
notes_list = []
current_note = None

sift = cv2.xfeatures2d.SIFT_create()

def compute_homography(image, template_path, callback, debug=False):
    points_list = []
    #img_final = cv2.imread(image_path, 1) # Displayed image

    img1 = cv2.imread(template_path, 0)   # Matching templates
    img2 = image               # Image to compute

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)

    ended = False

    while not ended:
        points = find_match(img1, kp1, des1, img2, debug)

        if points is not None:
            points_list.append(points)              # Memorise points for other external usages
            img2 = cv2.fillPoly(img2, points, 255)  # Fill to mask and compute next search with same template
            callback(points)                        # Main callback to notify found and return points

        else:
            ended = True

    return points_list #img_final

# Fouded callback from homography
def callback_founded(points):
    global image_final

    # Draw Contour on image
    image_final = cv2.polylines(image_final, points, True, 255, 3, cv2.LINE_AA)  # Contour
    #cv2.imshow("Homography", image_final)
    cv2.waitKey(1)

    # Note program
    notes_list.append(current_note)
    print("->Founded a " + str(current_note.value) + " note.")

def do_homography(frame):
    for color, note in note_colors.items():
        for image_note_path in note.sides:
            global current_note
            current_note = note
            compute_homography(frame, image_note_path, callback_founded, debug=False)

    print("The image show a sum of : " + str(sum(note.value for note in notes_list)))

    cv2.waitKey(0)


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    do_homography(frame)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()