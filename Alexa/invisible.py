import time
import numpy as np 
import cv2

video = cv2.VideoCapture(0)

time.sleep(3)

count = 0 
background = 0 


# Capture the intial background so that program can use that as a reference to product the invisibility effect. 

for i in range(60):
    ret, background = video.read()
background = np.flip(background, axis = 1)

while (video.isOpened()):
    ret, img = video.read()
    if ret is None:
        print("Hi")
        continue

    count+=1
    img = np.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([100, 40, 40])        
    upper_red = np.array([100, 255, 255])
    # lower_red = np.array([0, 120, 50])
    # upper_red = np.array([10, 255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([155, 40, 40]) 
    upper_red = np.array([180, 255, 255]) 
    # lower_red = np.array([170, 120, 70])
    # upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    # Opening and dilating the mask. 
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    #mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1) 

    mask2 = cv2.bitwise_not(mask1)

    res2 = cv2.bitwise_and(img, img, mask = mask2)

    res1 = cv2.bitwise_and(background, background, mask=mask1)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Final Output", final_output)

    if cv2.waitKey(10) == ord('q'):
        break

cv2.destroyAllWindows() 
video.release()

 