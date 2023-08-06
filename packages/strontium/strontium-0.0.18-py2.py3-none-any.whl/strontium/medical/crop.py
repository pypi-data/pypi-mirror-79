import numpy as np 
import cv2
from utils import CoreTransformation

class Crop():
	def __init__(self, image:np.array, x, y):
		super(Crop, self).__init__()

	def __call__(self, image, x, y):
		return image[0:x, 0:y]

transformation = Crop
crop = CoreTransformation(p=0.5, construct_class=transformation)