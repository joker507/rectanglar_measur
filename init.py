"""
Filename: init.py
Usage: This script will measure different objects in the frame using a reference object of known dimension. 
The object with known dimension must be the leftmost object.
Author: Shashank Sharma
"""
from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import sys
import os

# Function to show array of images (intermediate results)
def show_images(images):
	for i, img in enumerate(images):
		cv2.imshow("image_" + str(i), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def measure_w_h(img_path):
			
	# Read image and preprocess
	image = cv2.imread(img_path)

	# print("image size:", image.shape)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# show_images([gray])
	blur = cv2.GaussianBlur(gray, (9, 9), 0)
	# show_images([gray])

	edged = cv2.Canny(blur, 50, 100)
	# show_images([edged])
	edged = cv2.dilate(edged, None, iterations=1)
	# show_images([edged])
	edged = cv2.erode(edged, None, iterations=1)
	# show_images([edged])

	#show_images([blur, edged])

	# Find contours
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts) #xianwu:返回轮廓

	# Sort contours from left to right as leftmost contour is reference object
	(cnts, _) = contours.sort_contours(cnts)

	# Remove contours which are not large enough
	cnts = [x for x in cnts if cv2.contourArea(x) > 100]
	cont_image = image.copy()
	cv2.drawContours(cont_image, cnts, -1, (0,255,0), 3)

	# show_images([cont_image])
	# print(len(cnts))

	# Reference object dimensions
	# Here for reference I have used a 2cm x 2cm square 左上角的
	ref_object = cnts[0]
	box = cv2.minAreaRect(ref_object)
	box = cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	box = perspective.order_points(box)
	(tl, tr, br, bl) = box
	# print("box:", box)
	dist_in_pixel = euclidean(tl, tr) #计算欧氏距离
	# print("dist in pixel :", dist_in_pixel)
	dist_in_cm = 2  #参照物长度
	pixel_per_cm = dist_in_pixel/dist_in_cm  #距离比例  pixel_per_cm = a/2 = b/x  => x =b/pixe... 
	# print("pixel:", pixel_per_cm)
	# Draw remaining contours
	# print("cnts number :", len(cnts))
	for cnt in cnts:
		print("process step")
		box = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(box)
		box = np.array(box, dtype="int")
		box = perspective.order_points(box)
		(tl, tr, br, bl) = box
		cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
		mid_pt_horizontal = (bl[0] + int(abs(br[0] - bl[0])/2), bl[1] + int(abs(br[1] - bl[1])/2))
		mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0])/2), tr[1] + int(abs(tr[1] - br[1])/2))
		wid = euclidean(tl, tr)/pixel_per_cm
		ht = euclidean(tr, br)/pixel_per_cm
		# print(wid,ht)
		cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
		cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

	return image


if __name__ == "__main__":
		
	img_path = ''
	op_dir = 'output'

	try:
		img_path = sys.argv[1]
		print(img_path)
	except IndexError:
		print("参数传输错误， 应该为：python init.py test.jpg")
		exit(0)

	if not os.path.exists(op_dir):
		os.makedirs(op_dir)

	image = measure_w_h(img_path)

	cv2.imwrite(op_dir + '/result.jpg', image)

	show_images([image])

