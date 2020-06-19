# Instagramizer

This is a Python 3 script which essentially automates what I was doing by hand before in GIMP. It takes two arguments: the first is the image to 'instagramify' and the second OPTIONAL argument is the pixel radius of the gaussian blur applied to the background. The default is . Ex:

`python3 instagramizer.py mycoolphoto.jpg 10`

This will create an instagramized photo under the same directory with the name `instagramized_mycoolphoto.jpg`.

## General Process

Scale image to 2048px. If the photo is landscape, that means the horizontal side should go to 2048 as background, and overlayed with the photo with _height_ set to 2048px.

Vice versa for portrait photos.

Via some simple math, the image is pasted in a centered fashion over the background image, which is just the same image, but covering the 2048 x 2048 square, and blurred for nice effect.

That's it. Enjoy!