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

![Image](http://url/to/img.png)
