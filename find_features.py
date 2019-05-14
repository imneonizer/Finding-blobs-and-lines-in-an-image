import cv2
import numpy as np
import os
import time
import imutils
import math

os.system('color 0a')

def main():
	try:
		st = time.time()
		final = find('images/unknown-3.jpg')
		et = time.time()
		print()
		print('Time Elapsed: '+str(round(et-st,2))+' sec')
		cv2.imwrite("output/detected_feature.png", final)
		cv2.imshow('Final', final)
		cv2.waitKey(0)
		print()
		os.system('pause')
	except Exception as e:
		print(e)
		os.system('pause')


def find(img):
	print('>> Reading: '+img)
	image = cv2.imread(img)
	o_image = image

	print('>> Converting to Grayscale')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	print('>> Applying Gaussian Blur')
	blurred = cv2.GaussianBlur(gray, (11, 11), 5)

	kernel = np.ones((10,10), np.uint8)
	print('>> Applying Erosion')
	img_erosion = cv2.erode(blurred, kernel, iterations=5)
	print('>> Applying Dilation')
	img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
	
	filteration = img_dilation
	print('>> Applying OTSU Thresholding')
	ret, thresh = cv2.threshold(filteration, 0, 255, 
                            cv2.THRESH_OTSU)
	# Noise removal using Morphological closing operation
	print('>> Filling up Gap Holes')
	kernel = np.ones((3, 3), np.uint8) 
	closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, 
	                            kernel, iterations = 1)  
	dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0) 
	ret, fg = cv2.threshold(dist_transform, 0.05
	                        * dist_transform.max(), 255, 0)
	#dilating the mask
	print('>> Dilating, Over Filled Gap Holes')
	kernel = np.ones((10, 10), np.uint8)
	mask = cv2.dilate(fg, kernel, iterations=5)
	mask = np.uint8(mask)

	print('>> Masking out ROI')
	masked = cv2.bitwise_and(image,image,mask = mask)

	cv2.imwrite('output/mask.png', mask)
	cv2.imwrite('output/masked.png', masked)

	#after masking roi, let mask out lines============================================
	print('>> Using Masked ROI')
	image = masked
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	kernel = np.ones((3,3), np.uint8)
	img_erosion = cv2.erode(blurred, kernel, iterations=3)
	img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)

	kernel = np.ones((3,3), np.uint8)
	img_erosion = cv2.erode(img_dilation, kernel, iterations=1)

	filteration = img_erosion
	thresh = cv2.adaptiveThreshold(filteration,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
	            cv2.THRESH_BINARY_INV,5,3)
	print('>> Image Segmentation Going on')


	# Noise removal using Morphological closing operation
	print('>> Removing Noise')
	kernel = np.ones((4, 4), np.uint8) 
	closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, 
	                            kernel, iterations = 1) 
	
	  
	# Finding foreground area 
	dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0) 
	ret, fg = cv2.threshold(dist_transform, 0.02
	                        * dist_transform.max(), 255, 0)

	#dilating the mask
	kernel = np.ones((2, 2), np.uint8)
	mask = cv2.dilate(fg, kernel, iterations=3)
	thresh = np.uint8(mask)


	#Blob detection===================================================
	print('>> Finally Detecting Features')
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

	print('>> Everything done, Saving Output')
	return o_image

#=======================================================================================
if __name__ == '__main__':
	main()