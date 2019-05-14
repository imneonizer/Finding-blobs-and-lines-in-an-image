# Finding-blobs-and-lines-in-an-image
## Introduction
In this tutorial  we are going to find blobs and lines in an image and their sizes in pixels
> It is a part of assignment where the task was to detect,
> small blobs and lines and to find their size
> i applied some erosion and dilation followed by gaussian blur
> to mask out unwanted part from the image
> more over the blobs were placed on a plate of mono color
> so i tried to find the largest regualar shape in the image and masked it out.

After that, with the help of little thresholding and contour tracing i was able to find the
blobs but the problem here was.. there were unwanted blobs too so i need to filter them out aswell.
the trick that i applied here was to use a conditional statement to mark down only those areas as blobs
whose ``height, width, area, and perimeter`` matched the threshold.

## Required Modules
```
>> pip install opencv-contrib-pyton
>> pip install imutils
>> pip install numpy
```

## Here are the input images
![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/assets/input.png)

## Step 1 : Finding the largeset contour shape in the image
> In our case it is the region of interest for our object detection
so let's have the example of ``Unknown-3.jpg`` 
when i applied ``OTSU_Binarization`` and adaptive thresholding the result looked somethig like this

![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/assets/gap.png)

## Step 2 : Filling the Gaps
To fill up the gaps i used some Morphological Operations..

```
kernel = np.ones((3, 3), np.uint8) 
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 1)  
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0) 
ret, fg = cv2.threshold(dist_transform, 0.05* dist_transform.max(), 255, 0)

kernel = np.ones((10, 10), np.uint8)
mask = cv2.dilate(fg, kernel, iterations=5)
mask = np.uint8(mask)
```
> After which i achieved this.

![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/assets/gap_filled.png)

And so to carry on the task the next thing to work upon was to mask out the ``ROI`` from the original image.
and so i used this ``bitwise_and()`` operation
```
masked = cv2.bitwise_and(image,image,mask = mask)
```
Which surely worked out very well, and i was able to mask out the region of interest from the original image
> and the perk of using image masking is we don't need to deal with unwanted part of the image,
> that might can cause a lot of trouble while isolating object of our interest.
The masked out image looked something like this.
![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/output/masked.png)

Now from here the Interesting part start, and surely that is to detect the blobs and lines
so we need to detect them first before measuring their sizes and finding their coordinates.
> Again i used a set of operation like, ``Blurring > Erosion > Dilation`` and finally Contour tracing on top of Thresholded image

Below is the code for the same
```
blurred = cv2.GaussianBlur(thresh, (9, 9), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

#mask for final extraction
height,width,depth = o_image.shape

mask = np.zeros((height,width))

# loop over the contours
for c in cnts:
	x,y,w,h = cv2.boundingRect(c)
	area = cv2.contourArea(c)
	perimeter = cv2.arcLength(c,True)
	# compute the center of the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	if   w<200 and h<500 and perimeter>200 and perimeter<310 and area <2000: #condition for both
		if w<120:#condition for line
			# draw the contour and center of the shape on the image
			c[:] = [x - 5 for x in c] #contour position adjustment
			cv2.drawContours(o_image, [c], -1, (0, 0, 255), 2)#line red
			if h>w:
				#print('h>w')
				c_text = str('length: '+str(h)+' px')
				cv2.putText(o_image, c_text, (cX - 50, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 0)
			else:
				#print('w>h')
				c_text = str('length: '+str(w)+'px')
				cv2.putText(o_image, c_text, (cX - 20, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 0)
	if w> 10 and h<30 and area<900 and area>100:
		r = math.sqrt(area / math.pi)-2
		d = 2*round(r,2)
		#print(r)
		cv2.circle(o_image, (cX-3, cY-5), 10, (0, 255, 255), 2)#circle in yellow
		c_text = str('d = '+str(d)+'px')
		#c_text = str((cX-3 , cY-5 ))
		cv2.putText(o_image, c_text, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 0)
```
> Here is the step by step inter processed images by the program
![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/assets/masks.png)

> Finally when everything was done. it shows a output like this.
![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/assets/output.png)

> The program also saves the output image to the output folder with the
> detected contours and the sizes of the detected blobs and lines transcribed on to the image itself
![Image](https://github.com/imneonizer/Finding-blobs-and-lines-in-an-image/blob/master/output/detected_feature.png)

Hope you Enjoyed the Explaination, By the way i also tried to keep the most of the important part of the image inside
a try and catch block so that it don't interrupt abnormally, in case any error occurs.
along with it i tried to implement a time logging trick so as to check how fast the code is able to process the image.

Thanks for Reading
Nitin Rai
Contact: mneonizer@gmail.com
