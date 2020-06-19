import sys
import os
from PIL import Image, ImageDraw, ImageFilter

INSTAGRAM_PHOTO_SIZE = 2048

if len(sys.argv) > 3:
    print("Too many arguments provided. Exiting.")
    sys.exit()

if len(sys.argv) == 3:
    IMAGE_FILE = sys.argv[1]
    GAUSSIAN_BLUR_RADIUS = int(sys.argv[2])
elif len(sys.argv) == 2:
    IMAGE_FILE = sys.argv[1]
    GAUSSIAN_BLUR_RADIUS = 15
else:
    print("Not enough arguments provided. Exiting.")
    sys.exit()

# Open two versions of the image - one for the actual image to show and one to use as background
image = Image.open(IMAGE_FILE)
imageBackground = Image.open(IMAGE_FILE)

# some math
width, height = image.size
if width > height:
    ratio = width / height
else:
    ratio = height / width
incRatioSize = int(round(INSTAGRAM_PHOTO_SIZE * ratio))
decRatioSize = int(round(INSTAGRAM_PHOTO_SIZE / ratio))
x = int(round((incRatioSize - INSTAGRAM_PHOTO_SIZE) / 2))
y = int(round((INSTAGRAM_PHOTO_SIZE - decRatioSize) / 2))

# Prepare image and background sizes - background fills 2048 square, image is centered on it
if width > height:
    # Image background goes to height of instagram square
    imageBackground = imageBackground.resize((incRatioSize,INSTAGRAM_PHOTO_SIZE))

    # Image width goes to width of instagram square, height becomes the decreased ratio
    image = image.resize((INSTAGRAM_PHOTO_SIZE, decRatioSize))
    
    # Blur image background
    imageBackground = imageBackground.filter(ImageFilter.GaussianBlur(GAUSSIAN_BLUR_RADIUS))

    # see calculation above for x and y
    imageBackground.paste(image, (x, y))

    # crop out the desired 2048 x 2048 square
    imageBackground = imageBackground.crop((x, 0, x + INSTAGRAM_PHOTO_SIZE, INSTAGRAM_PHOTO_SIZE))
else:
    # Image background goes to width of instagram square
    imageBackground = imageBackground.resize((INSTAGRAM_PHOTO_SIZE, incRatioSize))

    # Image height goes to height of instagram square, width becomes the decreased ratio
    image = image.resize((decRatioSize, INSTAGRAM_PHOTO_SIZE))

    # Blur image background
    imageBackground = imageBackground.filter(ImageFilter.GaussianBlur(GAUSSIAN_BLUR_RADIUS))

    # and its starting x,y coordinates for paste inverse of that of other configuration
    imageBackground.paste(image, (y, x))

    # crop out the desired 2048 x 2048 square
    imageBackground = imageBackground.crop((0, x, INSTAGRAM_PHOTO_SIZE, x + INSTAGRAM_PHOTO_SIZE))

# save file to desktop
imageBackground.save(os.getcwd() + '/instagramize_' + sys.argv[1])

print("Done. Image exported to " + 'instagramize_' + sys.argv[1])








