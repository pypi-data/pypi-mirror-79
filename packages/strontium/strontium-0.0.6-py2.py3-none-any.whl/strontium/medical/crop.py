import numpy as np 
import cv2
from utils import CoreTransformation

class Crop():
	def __init__(self, image:np.array, x, y):
		super(Crop, self).__init__()
		self.image = image
		self.x     = x
		self.y     = y

	def __call__(self):
		return self.image[0:self.x, 0:self.y]

transformation = Crop()
crop = CoreTransformation(p=0.5, construct_class=transformation)