# Whiteboard
In this project, we are trying to create a white board using colour and edge detection. 
1) Black colour is detected, set the RBG ranges according to your surroundings, the range I used will not neccesarily works for everyone
2) Create the mask with the range mentioned in the above step and slice your frame to get only the Region of Intrest(ROI). Here I used a 400*400 rectangle 
3) Now that we have our ROI and a black object in that region, its time to get the edges.
4) We use contours for the edge detections, as our mask has only 2 values 0 for non black regions and 255 for black regions, create a threshold accordingly.
5) Using cv2.findcontours(), we'll get the indices of the edges detected. 
6) Extract the indices who's area is more than 3000. This value is not standard, it worked for me.
7) Now, compute the mid point taking top-left and bottom-right point. 
8) This point will be our cursor for drawing. 
9) Take a 3D numpy array with the shape same as ROI and 3 channels. fill all the values as (255,255,255)(rgb for white)
10) Now draw 4 circles 3 of them are for R, G, B colors and other circle to clear the screen 
11) Finally, WHenever our computed cursor hovers over these circles, either the colour is changed or screen is cleared. 
