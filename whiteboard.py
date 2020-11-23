import cv2
import numpy as np

camera = cv2.VideoCapture(0)
white = np.zeros((400,400,3),dtype='uint8')
white.fill(255)
RED_CENTER = (40,20)
GREEN_CENTER = (90,20)
BLUE_CENTER = (140,20)
START_CENTER = (370,30)
COLOR_RADIUS = 20
START_RADIUS = 30
PLAY = False
COLOR = (0,0,0)
def get_mask(frame):
    hsv = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([115, 118, 41])
    mask = cv2.inRange(hsv, lower, upper)
    return mask
def get_indices(frame,mask):
    _, thresh = cv2.threshold(mask, 170, 255, 0)
    contours, hire = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    min_x, min_y = (1000,1000)
    max_x, max_y = (0,0)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area<3000:continue
        for a in contour:
            for b in a:
                if min_x > b[0]:(min_x, min_y) = (b[0], b[1])
                if min_x == b[0] and min_y > b[1]:(min_x, min_y) = (b[0], b[1])

                if max_x < b[0]:(max_x, max_y) = (b[0], b[1])
                if max_x == b[0] and max_y > b[1]:(max_x, max_y) = (b[0], b[1])
    return [min_x,min_y,max_x,max_y]
def check_start(x,y):
    (x1,y1) = START_CENTER
    return (x-x1) * (x-x1) + (y-y1) * (y-y1) <= START_RADIUS*START_RADIUS
def check_red(x,y):
    (x1, y1) = RED_CENTER
    return (x - x1) * (x - x1) + (y - y1) * (y - y1) <= COLOR_RADIUS * COLOR_RADIUS
def check_green(x,y):
    (x1, y1) = GREEN_CENTER
    return (x - x1) * (x - x1) + (y - y1) * (y - y1) <= COLOR_RADIUS * COLOR_RADIUS
def check_blue(x,y):
    (x1, y1) = BLUE_CENTER
    return (x - x1) * (x - x1) + (y - y1) * (y - y1) <= COLOR_RADIUS * COLOR_RADIUS
while True:
    _,frame = camera.read()
    f = frame[100:500, 100:500]
    mask = get_mask(f)
    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    cv2.rectangle(frame,(100,100),(500,500),(255,0,0),2) #ROI


    indices = get_indices(f,mask)
    mid_x, mid_y = ((indices[0]+indices[2])//2, (indices[1]+indices[3])//2)

    if check_start(mid_x,mid_y):
        if PLAY:PLAY = False
        else: PLAY = True
    if check_red(mid_x,mid_y):
        COLOR = (0,0,255)
    if check_green(mid_x,mid_y):
        COLOR = (0,255,0)
    if check_blue(mid_x,mid_y):
        COLOR = (255,0,0)
    if mid_x != 500:
        if not PLAY:
            white = np.zeros((400,400,3),dtype='uint8')
            white.fill(255)
        cv2.rectangle(white, (mid_x, mid_y), (mid_x + 5, mid_y + 5), COLOR, 3)

    cv2.circle(white, RED_CENTER, 20, (0, 0, 255), -1)
    cv2.circle(white, GREEN_CENTER, 20, (0, 255, 0), -1)
    cv2.circle(white, BLUE_CENTER, 20, (255, 0, 0), -1)
    cv2.circle(white, START_CENTER, 30, (0, 0, 0), -1)
    cv2.circle(f,(mid_x,mid_y),5,(255,0,0),-1)

    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)
    cv2.imshow("white",white)
    if cv2.waitKey(1) == ord('q'):break

