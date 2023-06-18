from PIL import Image
import os

# Set the directory containing the images
directory = "testsets/MedSetA/MUSC1"

# Create a new directory to save the modified images
new_directory = "testsets/MedSet/MUSC1"
if not os.path.exists(new_directory):
    os.makedirs(new_directory)

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Open the image
        image = Image.open(os.path.join(directory, filename))

        # Remove the alpha channel from the image
        image = image.convert('RGB')

        # Save the modified image to the new directory
        image.save(os.path.join(new_directory, filename))
