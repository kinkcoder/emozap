#https://github.com/oarriaga/face_classification

# This library lets you measure time
from time import time

import json

import os
from subprocess import check_output

# mss is a cross platform library for taking screenshots
# i use it to indirectly get an image from the webcam
import mss
import mss.tools

sct = mss.mss()

# The screen part to capture
monitor = {"top": 20, "left": 0, "width": 640, "height": 480}
output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

print("SMILE :)")

fps = 0
def run():
	global fps
	i = 0
	start = time()

	while True:
		# Grab the data
		sct_img = sct.grab(monitor)

		# Save the picture to a file and scale it down
		mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
		os.system(f"convert {output} -resize 320x240\> {output}")

		# Send a POST request to the docker server

		# The endpoint /classifyImage returns an annotated image
		# Remove -s and Add -v for verbose output
		#os.system(f"curl -s -F image=@{output} http://localhost:4000/classifyImage > classified.png ")

		# The endpoint /classifyText only returns a list of detected emotions
		result = check_output(f"curl -s -F image=@{output} http://localhost:4000/classifyText", shell=True)
		array = json.loads(result)

		if len(array) > 0:
			track(array)

		if i == 15:
			i = 0
			start = time()
		else:
			i += 1
			fps = i/(time()-start)

# If you haven't smiled for the last <n> seconds, you get zapped!
smilewindow = 5

lastsmiled = None
def track(array):
	global lastsmiled
	happy = "happy" in array

	if lastsmiled is not None:
		estimated_zap = smilewindow - (time() - lastsmiled)
		zapstring = f"Zap in: {estimated_zap:.2f}" if estimated_zap > 0 else "ZAP!"
		print(f"{fps:.2f} FPS\t| Happy: {happy}\t| {zapstring}")

	if happy:
		lastsmiled = time()
	elif lastsmiled is not None:
		#print(happy, time()-lastsmiled)
		if time() - lastsmiled > smilewindow:
			zap()

def zap():
	#print("ZAP!")
	pass

run()
