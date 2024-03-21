import os
import random
from PIL import Image
import shutil
import re

def process_images_in_folder(folder_path, angle_ranges):
    # Regular expression pattern to match files ending with '_Y.ext' where Y is a digit
    skip_pattern = re.compile(r'_\d\.\w+$')

    # Iterate over all image files in the given folder
    for filename in os.listdir(folder_path):
        # Skip files that match the skip_pattern
        if skip_pattern.search(filename):
            #print(f"Skipping file: {filename}")
            continue

        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            original_filename = os.path.splitext(filename)[0]
            file_extension = os.path.splitext(filename)[1]

            # Check if the file has already been processed
            if os.path.exists(os.path.join(folder_path, f"{original_filename}_1{file_extension}")) and \
               os.path.exists(os.path.join(folder_path, f"{original_filename}_8{file_extension}")):
                #print(f"Skipping already processed file: {filename}")
                continue

            file_path = os.path.join(folder_path, filename)

            print("Animating new image " + filename)
            with Image.open(file_path) as img:
                # Generate random angles from the given range
                angles = [random.randint(*range_pair) for range_pair in angle_ranges]

                # Rotate, resize, and save each image
                for i, angle in enumerate(angles, start=1):
                    rotated_img = img.rotate(angle, expand=True)
                    resized_img = rotated_img.resize((96, 96))  # Resize the image to 96x96

                    new_filename = f"{original_filename}_{i}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_filename)
                    resized_img.save(new_file_path, 'PNG')

                # Copy the source image to source_filename_0.ext
                shutil.copy(file_path, os.path.join(folder_path, f"{original_filename}_0{file_extension}"))

# Define different angle ranges
angle_ranges_7 = [(-1, 1), (-4, -2), (-7, -5), (-4, -2), (-1, 1), (2, 4), (5, 7), (2, 4)]
angle_ranges_10 = [(-1, 1), (-6, -3), (-10, -7), (-6, -3), (-1, 1), (3, 6), (7, 10), (3, 6)]
angle_ranges_15 = [(-2, 2), (-9, -5), (-15, -11), (-9, -5), (-2, 2), (5, 9), (11, 15), (3, 8)]
angle_ranges_25 = [(-3, 3), (-13, -8), (-25, -18), (-12, -5), (-3, 3), (8, 13), (18, 25), (5, 12)]

# Define folder paths for each angle range
folder_and_angle_ranges = [
    (angle_ranges_7, "ToneImg/animated_players_7"),
    (angle_ranges_10, "ToneImg/animated_players_10"),
    (angle_ranges_15, "ToneImg/animated_players_15"),
    (angle_ranges_25, "ToneImg/animated_players_25"),
]

print("Rotating and resizing images...")

# Loop through each angle range and corresponding folder
for angle_range, folder_path in folder_and_angle_ranges:
    process_images_in_folder(folder_path, angle_range)

print("Done.")