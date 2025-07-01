import sys
import os
import io
from PIL import Image, ImageFilter, ImageDraw, ImageCms

# allow massive images - NOTE: IN PRODUCTIVE SCENARIOS THIS CAN ALLOW COMPRESSION BOMB EXPLOITS!!!
Image.MAX_IMAGE_PIXELS = 20000*20000

# constants
MAX_ARGUMENTS = 4
INSTAGRAM_PHOTO_SIZE = 2048

# argument defaults, no border, no background blur
BACKGROUND_GAUSSIAN_BLUR_RADIUS = 0
BORDER_SIZE = 0

# Check for help flag
if len(sys.argv) > 1 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
    print("Instagramize - Convert images to Instagram-ready 2048x2048 squares")
    print("")
    print("Usage:")
    print("  python3 instagramize.py <image_file> [blur_radius] [border_size]")
    print("")
    print("Arguments:")
    print("  image_file    (Required) Path to the image file to process")
    print("  blur_radius   (Optional) Gaussian blur radius for background (default: 0)")
    print("  border_size   (Optional) White border size around the image (default: 0)")
    print("")
    print("Examples:")
    print("  python3 instagramize.py mycoolphoto.jpg")
    print("    - Basic conversion with no blur or border")
    print("")
    print("  python3 instagramize.py mycoolphoto.jpg 15")
    print("    - Add 15px gaussian blur to the background")
    print("")
    print("  python3 instagramize.py mycoolphoto.jpg 15 10")
    print("    - Add 15px blur and 10px white border")
    print("")
    print("  python3 instagramize.py nature.jpg 20 5")
    print("    - Heavy blur (20px) with small border (5px)")
    print("")
    print("Output:")
    print("  Creates 'instagramize_<original_filename>' in the current directory")
    print("  Final image will be 2048x2048 pixels, perfect for Instagram")
    sys.exit()

if len(sys.argv) > MAX_ARGUMENTS:
    print("Too many arguments provided. Exiting.")
    sys.exit()
if len(sys.argv) == MAX_ARGUMENTS:
    IMAGE_FILE = sys.argv[1]
    BACKGROUND_GAUSSIAN_BLUR_RADIUS = int(sys.argv[2])
    BORDER_SIZE = int(sys.argv[3])
elif len(sys.argv) == MAX_ARGUMENTS - 1:
    IMAGE_FILE = sys.argv[1]
    BACKGROUND_GAUSSIAN_BLUR_RADIUS = int(sys.argv[2])
elif len(sys.argv) == MAX_ARGUMENTS - 2:
    IMAGE_FILE = sys.argv[1]
else:
    print("Not enough arguments provided. Exiting.")
    sys.exit()

# based on passed border and instagram size, this is the max allowed side (though it could be width or height side)
max_allowed_size = int(round(INSTAGRAM_PHOTO_SIZE - (BORDER_SIZE*4)))

# Open two versions of the image - one for the actual image to show and one to use as background
image = Image.open(IMAGE_FILE)
imageBackground = Image.open(IMAGE_FILE)

# Try to get the original color profile so it can be preserved - otherwise just set to an empty string
try:
    iccProfile = image.info.get('icc_profile')
    iccBytes = io.BytesIO(iccProfile)
    originalColorProfile = ImageCms.ImageCmsProfile(iccBytes)
except OSError:
    originalColorProfile = ''

# some math
original_image_width, original_image_height = image.size
image_aspect_ratio = original_image_width / original_image_height

# Calculate image dimensions
if original_image_width > original_image_height:
    image_resize_width = max_allowed_size
    image_resize_height = int(round(image_resize_width/image_aspect_ratio))
else:
    image_resize_height = max_allowed_size
    image_resize_width = int(round(image_resize_height*image_aspect_ratio))

# coordinates to paste (center imagine in square just subtract dimensions and divide by 2)
paste_x = int(round((INSTAGRAM_PHOTO_SIZE - image_resize_width) / 2))
paste_y = int(round((INSTAGRAM_PHOTO_SIZE - image_resize_height) / 2))

# Calculate background dimensions to ensure it covers the entire canvas
if image_aspect_ratio >= 1:  # landscape or square
    # For landscape images, make height = INSTAGRAM_PHOTO_SIZE and scale width proportionally
    background_resize_height = INSTAGRAM_PHOTO_SIZE
    background_resize_width = int(round(INSTAGRAM_PHOTO_SIZE * image_aspect_ratio))
    # Crop from the sides
    background_crop_dimension = int(round(abs(INSTAGRAM_PHOTO_SIZE - background_resize_width) / 2))
    background_crop_tuple = (background_crop_dimension, 0, background_crop_dimension + INSTAGRAM_PHOTO_SIZE, INSTAGRAM_PHOTO_SIZE)
else:  # portrait
    # For portrait images, make width = INSTAGRAM_PHOTO_SIZE and scale height proportionally
    background_resize_width = INSTAGRAM_PHOTO_SIZE
    background_resize_height = int(round(INSTAGRAM_PHOTO_SIZE / image_aspect_ratio))
    # Crop from top and bottom
    background_crop_dimension = int(round(abs(INSTAGRAM_PHOTO_SIZE - background_resize_height) / 2))
    background_crop_tuple = (0, background_crop_dimension, INSTAGRAM_PHOTO_SIZE, background_crop_dimension + INSTAGRAM_PHOTO_SIZE)

# Draw white background (if border size is 0, this will be immediately rewritten in either of the paste methods below, so 'safe' to do always)
white_rectangle_x0 = paste_x - BORDER_SIZE
white_rectangle_y0 = paste_y - BORDER_SIZE
white_rectangle_x1 = white_rectangle_x0 + image_resize_width + BORDER_SIZE + BORDER_SIZE
white_rectangle_y1 = white_rectangle_y0 + image_resize_height + BORDER_SIZE + BORDER_SIZE - 1

# Resize background
imageBackground = imageBackground.resize((background_resize_width, background_resize_height))

# Resize image
image = image.resize((image_resize_width, image_resize_height))

# Blur image background
if BACKGROUND_GAUSSIAN_BLUR_RADIUS > 0:
    imageBackground = imageBackground.filter(ImageFilter.GaussianBlur(BACKGROUND_GAUSSIAN_BLUR_RADIUS))

# crop out the desired 2048 x 2048 square
imageBackground = imageBackground.crop(background_crop_tuple)

# now create a draw object after the crop has been made
imageBackgroundDraw = ImageDraw.Draw(imageBackground)

# First draw the white background if a border is given - done before image paste
imageBackgroundDraw.rectangle([white_rectangle_x0, white_rectangle_y0, white_rectangle_x1, white_rectangle_y1], fill="white")

# and its starting x, y coordinates for paste, inverse of that of the other configuration
imageBackground.paste(image, (paste_x, paste_y))

# dispose of the draw object
del imageBackgroundDraw

# Save the file to the desktop, preserving the color profile of the image
if originalColorProfile != '':
    imageBackground.save(os.getcwd() + '/instagramize_' + sys.argv[1], icc_profile=originalColorProfile.tobytes())
else:
    imageBackground.save(os.getcwd() + '/instagramize_' + sys.argv[1])

print("Done. Image exported to " + 'instagramize_' + sys.argv[1])
