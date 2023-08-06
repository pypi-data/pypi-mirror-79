import numpy as np 
import cv2
import math
import random
import warnings
from ..utils import *
from skimage.transform import resize

class Crop:
	def __call__(self, image, x, y):
		rd = resize(image, (x, y))
		return rd
		
class WindowDicom:
	def window_image(img,window_center,window_width,intercept,slope):

		img = (img*slope + intercept)
		minimg = window_center - window_width//2
		maximg = window_center + window_width//2
		img[img<minimg] = minimg
		img[img>maximg] = maximg

		img = (img - minimg) / (maximg - minimg)
		return img

	def get_first_of_dicom_field_as_int(x):
    #get x[0] as in int is x is a 'pydicom.multival.MultiValue', otherwise get int(x)
		if type(x) == pydicom.multival.MultiValue:
			return int(x[0])
		else:
			return int(x)

	def get_windowing(data):
		dicom_fields = [data[('0028','1050')].value, #window center
                    data[('0028','1051')].value, #window width
                    data[('0028','1052')].value, #intercept
                    data[('0028','1053')].value] #slope
		return [get_first_of_dicom_field_as_int(x) for x in dicom_fields]


	def __call__(dicom_file, param_1, param_2):
		try:
			window_center , window_width, intercept, slope = get_windowing(dicom_file)
			img                                            = dicom_file.pixel_array
			dls                                            = window_image(img, param_1, param_2, intercept, slope)


    
transformation = Crop()
Crop = CoreTransformation(p=0.5, construct_class=transformation)
transformation = WindowDicom()
WindowDicom = CoreTransformation(p=0.5, construct_class=transformation)