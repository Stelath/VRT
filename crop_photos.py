from PIL import Image
import os

# Set the directory containing the images
directory = "testsets/MedSet/MUSC2"
cropped_directory = directory + "_cropped"

# Create the directory if it doesn't exist
if not os.path.exists(cropped_directory):
    os.makedirs(cropped_directory)

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Open the image
        image = Image.open(os.path.join(directory, filename))

        # Get the current size of the image
        width, height = image.size

        desired_width = width//8*8
        desired_height = height//8*8

        # Crop the image to removing rows and columns as needed to make the dimensions multiples of 8
        image = image.crop((0, 0, desired_width, desired_height))

        # Save the modified image
        image.save(os.path.join(cropped_directory, filename))