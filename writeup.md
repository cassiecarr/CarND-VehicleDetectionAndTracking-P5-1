# Writeup: Vehicle Detection Project

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, apply a color transform and append binned color features, as well as histograms of color, to the HOG feature vector. 
* Implement a sliding-window technique and use trained classifier to search for vehicles in images.
* Run pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

[//]: # (Image References)
[image1]: ./output_images/training_images/image0117.png
[image2]: ./output_images/training_images/extra224.png
[image3]: ./output_images/hog_test_images/image0117.png
[image4]: ./output_images/hog_test_images/extra224.png
[image5]: ./output_images/window_images/test5.jpg
[image6]: ./output_images/heat_images/test5.jpg
[image7]: ./output_images/test5.jpg
[image8]: ./output_images/window_images/test4.jpg
[image9]: ./output_images/window_images/test6.jpg


---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Vehicle-Detection/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Histogram of Oriented Gradients (HOG)

#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

During training, HOG features and spatial features were extracted using the `extract_features` function, starting in line 61 of [VehicleDetection.py](VehicleDetection.py). `extract_features` can be found in [VehicleDetectionUtils.py](VehicleDetectionUtils.py) line 44. 

Training images of `vehicles` and `non-vehicles` were read and used as parameters for the `extract_features` function. Here is an example of one of each of the `vehicle` and `non-vehicle` classes:

![alt text][image1] ![alt text][image2]

In order to determine the most effective HOG parameters for training, I tested various colorspaces and HOG parameters such as `orientations`, `pixels_per_cell`, and `cells_per_block`.  I selected a set of `vehicle` and `non-vehicle` images to use for visualizing the effect each parameter had on the dataset. These can be found in the [output_images](output_images) folder. 

Here is an example using the 'YCrCb' color space and HOG parameters of `orientations=8`, `pixels_per_cell=(8, 8)` and `cells_per_block=(1, 1)`:

![alt text][image3] ![alt text][image4]

#### 2. Explain how you settled on your final choice of HOG parameters.

A selected set of `vehicle` and `non-vehicle` images were used to test and determine my final choice of HOG parameters. I experimented with colorspace first and used HOG visualizations to see what colorspaces and color channels provided the largest visual difference between `vehicle` and `non-vehicle` images. After narrowing in on 'YCrCb' and 'ALL' color channels, I experimented with `orientations`, `pixels_per_cell`, and `cells_per_block` parameters, fine tuning the level of detail to see what looked visually best. This was then followed by testing the parameters on video subclips to see how the parameters performed with the full pipeline. 

#### 3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

I trained a linear SVM using sklearn's `LinearSVC` function. This can be found in line 93 of [VehicleDetection.py](VehicleDetection.py). The data fed into the `LinearSVC` function is the output of the `extract_features` function scaled using sklearn's `StandardScaler` function. In order to improve the accuracy and performance of the classifier, the images were doubled and vertically flipped for a more augmented dataset. The base `vehicle` and `non-vehicle` datasets for the project were used and additional images were extracted from the Udacity dataset to help in the detection of white cars. 

### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

In order to determine where and what size of windows to use for my search, I reviewed the test images and the size of the vehicles at various points of the video and placed the sliding window search at these locations accordingly. Smaller windows were used towards the horizon and larger windows along the bottom of the image. The window sizes were defined in line 122 of [VehicleDetection.py](VehicleDetection.py). The `slide_window` function used to develop these windows can be found in line 108 of [VehicleDetectionUtils.py](VehicleDetectionUtils.py). 

The overlap selected was choosen by trial and error to see what value produced the best result. 

#### 2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

My final pipeline contains 'YCrCb' 3-channel HOG features, plus spatially binned color feature vector of the 'Cb' color channel.  In order to optimize my classifier and come to the final result, I experimented with different colorspaces and the number of color channels for HOG and spatial feature vectors. I tested using all color channels and individual color channels. In addition, I tested with histogram feature vectors but found this did not provide positive results.

Below are a few window images from my pipeline showing found vehicle windows in blue. Images like this were used in trial and error to see what set of parameters gave the best results. 

![alt text][image8]
![alt text][image9]

---

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)

Here's a [link to my video result](https://youtu.be/tqVbcKeqQzQ)

#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

In line 134 of [VehicleDetection.py](VehicleDetection.py) `hot_windows` are defined as the windows where vehicles are detected in the frame. In order to smooth out the vehicle bounding boxes and improve the robustness of the vehicle search, I created an array that saved the last 30 frames' `hot_windows` and all of these windows were used to create a heatmap of the image. This can be found starting in line 141 of [VehicleDetection.py](VehicleDetection.py). A threshold is then applied to this heatmap in line 161. Then, in line 171, the `draw_labeled_boxes` function is used to draw a single box on the image for each grouping on the heatmap. The details of this can be found in `draw_labeled_boxes` on line 255 of [VehicleDetectionUtils.py](VehicleDetectionUtils.py), where the heatmap labels are looped though and drawn. If the groupings were found to be a certain distance away from each other, they were combined into one grouping. 

##### Here is the window image of one of the test images:
![alt text][image5]

##### Here is the associated heatmap of that image:
![alt text][image6]

##### Here is the resulting bounding boxes drawn in the image:
![alt text][image7]

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

For this project, my main technique was experimenting with different parameters to find the best solution. I found along the way that it was very difficult to balance finding vehicles the entire way through the video without picking up false positives. I also faced issues with code performace. The pipeline used takes a large amount of time to run and hindered my testing. 

My pipeline will probably fail with videos of different settings and lighting. A more varied training set would be needed to make it more robust. In addition, because of performance issues, it would not be able to run in real time. In the future, I would like to work on improving the speed of my pipeline by running the 'get_hog_features' function only one time for each frame and by looking at groups of frames rather than looking at each individually. I am hoping this would also help eliminate some of the frames where the vehicle is occassionally lost.

