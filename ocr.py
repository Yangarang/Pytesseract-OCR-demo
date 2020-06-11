# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="",
    help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# remove 
elif args["preprocess"] == "blocks":
	# binary threshold again except reverse white and black
	thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
	# create a block size of 5x5
	blocks = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
	# remove all rectangles with a size under 5x5
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, blocks)
	# reverse white and black again
	gray = 255 - opening

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print("Read Text: \n" + text)
# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)


### call script: python ocr.py -i example_01.png -p thresh
### edited from https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/