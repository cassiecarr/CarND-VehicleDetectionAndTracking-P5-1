# Vehicle Detection

# Import packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import math 
import moviepy
from moviepy.editor import VideoFileClip
import glob

# Return color processed image with vehicle detection boxes overlaid
def process_image(image):

	return image

# Process test images with process image function
for filename in os.listdir("test_images/"):
    if filename.endswith(".jpg"): 
        # Identify the image
        image = mpimg.imread(os.path.join("test_images/", filename))
        output = bound_process_image(image)

        # Save the file as overlay
        mpimg.imsave((os.path.join("output_images/test_images_with_lane_line_overlay/", filename)),output)

# Process video with process image function
output = 'output.mp4'
clip = VideoFileClip("project_video.mp4")
output_clip = clip.fl_image(bound_process_image) 
output_clip.write_videofile(output, audio=False)