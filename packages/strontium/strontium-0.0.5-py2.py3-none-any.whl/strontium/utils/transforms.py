class CoreTransformation:

	def __init__(self, p, construct_class):
		super(Transformation, self).__init__()
		self.p = p
		self.construct_class = construct_class

	def __call__(self, image):
		if image == None:
			raise ValueError("You have improperly called the image constructor.")
		else:
			if self.construct_class == None:
				raise ValueError("Constructor improperly called, please retry by properly applying a constructor for the transformation.")
			else:
				try:
					return self.construct_class(image)
				except Exception:
					raise ValueError("Your constructor function has an error in it.")

			
class TwoImageTransformation:

	def __init__(self, p, construct_class):
		super(TwoImageTransformation, self).__init__()
		self.p = p
		self.construct_class = construct_class

	def __call__(self, image1, image2):
		if image == None:
			raise ValueError("You have improperly called the image constructor.")
		else:
			if self.construct_class == None:
				raise ValueError("Constructor improperly called, please retry by properly applying a constructor for the transformation.")
			else:
				try:
					return self.construct_class(image1, image2)
				except Exception:
					raise ValueError("Your constructor function has an error in it.")		