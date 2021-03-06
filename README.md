
## xianwu :
1. 图片上传 前景物体需要和背景物体有较大的差别，图片 左上角 要有一个2厘米的正方形 必须在最左边
2. 图片的大小建议在 < 1080

### 加上树莓派运行

在纯白底部载物台画有一个左上角有一个2cm的正方形作为标尺：



# Measure size of objects in an image using OpenCV 

The project provides a script to read an image and based on the dimensions of a reference object find the dimensions of other objects in a scene. The reference object must be the leftmost object in the scene. In sample images given, a box of dimension 2cm x 2cm is taken as a reference object.

For any other reference object provide actual width of the object. (change line 59 in file 'init.py')

### Constraints
1. Shadow effect: use dark braground
2. Object boundry: use contrasting background

## Getting Started

### Prerequisites
Python 3
Pip
OpenCV
Numpy

### Installing
For python and pip installation follow this blog
1. For windows
https://www.howtogeek.com/197947/how-to-install-python-on-windows/
2. For Linux
https://docs.python-guide.org/starting/install3/linux/

Other prerequisites:
- pip install numpy
- pip install opencv-python

## Algorithm
1. Image pre-processing
  - Read an image and convert it it no grayscale
  - Blur the image using Gaussian Kernel to remove un-necessary edges
  - Edge detection using Canny edge detector
  - Perform morphological closing operation to remove noisy contours

2. Object Segmentation
  - Find contours
  - Remove small contours by calculating its area (threshold used here is 100)
  - Sort contours from left to right to find the reference objects

3. Reference object 
  - Calculate how many pixels are there per metric (centi meter is used here)

4. Compute results
  - Draw bounding boxes around each object and calculate its height and width

## Results

![Result](images/img2.jpg?raw=true "Title")

## Authors

* **Shashank Sharma** 

## Acknowledgments

* https://www.pyimagesearch.com/





