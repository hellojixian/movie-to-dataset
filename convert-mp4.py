#!/usr/bin/env python3

import os
import sys
import moviepy.editor as mp
from PIL import Image
from tqdm import tqdm

desired_resolution = (614,480)

def take_screenshots(input_file, output_directory):
    # Load the MP4 file
    video = mp.VideoFileClip(input_file)

    # Calculate the duration of the video
    duration = video.duration

    # Iterate over 10-second intervals
    interval = 10
    for t in tqdm(range(0, int(duration), interval)):
        # Extract a frame at the current time
        frame = video.get_frame(t)

        # Convert the frame to a PIL Image object
        image = Image.fromarray(frame)

        # Calculate the desired width and height for cropping
        desired_width =  desired_resolution[0]
        desired_height = desired_resolution[1]
        zoom_rate = image.height / desired_height

        # Calculate the center crop coordinates
        left = int((image.width - desired_width * zoom_rate) / 2)
        upper = 0
        right = left + desired_width * zoom_rate
        lower = image.height

        # Crop the image while maintaining the aspect ratio
        cropped_image = image.crop((left, upper, right, lower))

        # Resize the cropped image to 512x512
        resized_image = cropped_image.resize(desired_resolution)

        # Save the image as a JPG file
        output_file = f"{output_directory}/screenshot_{t}.jpg"
        resized_image.save(output_file)

    # Close the video file
    video.reader.close()

# Path to the input MP4 file
input_file = sys.argv[2]
print(f"Input file: {input_file}")

# Output directory to save the screenshots
project_name = sys.argv[1]
output_directory = f'output/{project_name}'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Take screenshots from the MP4 file
take_screenshots(input_file, output_directory)