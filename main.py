import math

import struct

import sys

import time

from PIL import Image

# Define the ASCII characters to use for the video conversion

ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

# Function to convert a single image to ASCII

def image_to_ascii(image, width, height):

    # Resize the image and convert it to grayscale

    image = image.resize((width, height)).convert('L')

    # Convert each pixel to an ASCII character based on its brightness

    ascii_pixels = []

    for y in range(height):

        ascii_row = []

        for x in range(width):

            brightness = image.getpixel((x,y))

            ascii_index = math.ceil((brightness / 255) * (len(ascii_chars) - 1))

            ascii_row.append(ascii_chars[ascii_index])

        ascii_pixels.append(''.join(ascii_row))

    # Combine the ASCII characters into a single string

    ascii_art = '\n'.join(ascii_pixels)

    return ascii_art

# Function to convert a video file to ASCII frames

def video_to_ascii(video_file):

    # Open the video file and get its properties

    with open(video_file, 'rb') as f:

        f.seek(0, 2)

        file_size = f.tell()

        f.seek(0)

        width = struct.unpack('i', f.read(4))[0]

        height = struct.unpack('i', f.read(4))[0]

        frame_size = width * height * 3

        # Define the number of frames to process at a time

        frames_per_chunk = 100

        while True:

            # Read a chunk of frames from the video

            chunk_start = f.tell()

            chunk_data = f.read(frame_size * frames_per_chunk)

            if not chunk_data:

                break

            chunk_end = f.tell()

            # Convert each frame in the chunk to ASCII art

            for i in range(frames_per_chunk):

                # Calculate the offset of the current frame in the chunk

                frame_offset = i * frame_size

                # Extract the frame data from the chunk

                frame_data = chunk_data[frame_offset:frame_offset+frame_size]

                # Convert the frame data to a PIL Image object

                frame = Image.frombytes('RGB', (width, height), frame_data)

                # Convert the frame to ASCII art

                ascii_art = image_to_ascii(frame, 80, 60)

                # Print the ASCII art to the console

                sys.stdout.write('\033[2J\033[1;1H' + ascii_art)

                sys.stdout.flush()

            # Move the file pointer to the start of the next chunk

            f.seek(chunk_end)

            # Wait for the appropriate amount of time before displaying the next frame

            time.sleep(1/30)  # Assumes a frame rate of 30fps

    # Close the video file

    f.close()

# Convert the video file to ASCII art

video_to_ascii('video.mp4')
