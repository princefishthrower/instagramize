import sys
import os
from PIL import Image, ImageDraw, ImageFilter

INSTAGRAM_PHOTO_SIZE = 2048

if len(sys.argv) > 2:
    print("Too many arguments provided. Exiting.")
    sys.exit()

if len(sys.argv) == 2:
    IMAGE_FILE = sys.argv[1]
    GAUSSIAN_BLUR_RADIUS = sys.argv[2]
elif len(sys.argv) == 1:
    IMAGE_FILE = sys.argv[1]
    GAUSSIAN_BLUR_RADIUS = 25
else:
    print("Not enough arguments provided. Exiting.")
    sys.exit()

# Open two versions of the image - one for the actual image to show and one to use as background
image = Image.open(IMAGE_FILE)
imageBackground = Image.open(IMAGE_FILE)

# some math
width, height = image.size
ratio = width / height
incRatioSize = INSTAGRAM_PHOTO_SIZE * ratio
decRatioSize = INSTAGRAM_PHOTO_SIZE / ratio
x = (incRatioSize - INSTAGRAM_PHOTO_SIZE) / 2
y = (INSTAGRAM_PHOTO_SIZE - decRatioSize) / 2

# Prepare image and background sizes - background fills 2048 square, image is centered on it
if width > height:
    # Image background goes to height of instagram square
    imageBackground.resize(incRatioSize,INSTAGRAM_PHOTO_SIZE)
    
    # Blur image background
    blurredBackground = imageBackground.filter(ImageFilter.GaussianBlur(GAUSSIAN_BLUR_RADIUS))

    # Image width goes to width of instagram square, height becomes the decreased ratio
    image.resize(INSTAGRAM_PHOTO_SIZE, decRatioSize)

    # see calculation above for x and y
    blurredBackground.paste(image, (x, y))

    # crop out the desired 2048x2048 square
    blurredBackground.crop(x, 0, 2048, x + 2048)
else:
    # Image background goes to width of instagram square
    imageBackground.resize(incRatioSize, INSTAGRAM_PHOTO_SIZE)

    # Blur image background
    blurredBackground = imageBackground.filter(ImageFilter.GaussianBlur(GAUSSIAN_BLUR_RADIUS))

    # Image height goes to height of instagram square, width becomes the decreased ratio
    image.resize(decRatioSize, INSTAGRAM_PHOTO_SIZE)

    # and its starting x,y coordinates for paste inverse of that of other configuration
    blurredBackground.paste(image, (y, x))

    # crop out the desired 2048x2048 square
    blurredBackground.crop(0, x, x + 2048, 2048)

# save file to desktop
blurredBackground.save(os.getcwd() + 'instagramized_' + sys.argv[1])








