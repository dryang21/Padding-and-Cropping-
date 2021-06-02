# Padding and Cropping

For ten phases CXR.   
1.First padding all to sqaure.   
2.Use cv2 to find the largest bounding box which contains all lung region.   
3.Then shape the rectangle bounding box to a sqaure.  
4.Use the boundingbox to segment each phase.  
