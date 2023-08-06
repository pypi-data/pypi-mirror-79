class CoreTransformation:

	def __init__(self, p, construct_class):
		super(CoreTransformation, self).__init__()
		self.p = p
		self.construct_class = construct_class

	def __call__(self, *args):

		if self.construct_class == None:
			raise ValueError("Constructor improperly called, please retry by properly applying a constructor for the transformation.")
		else:
			try:
				return self.construct_class(*args)
			except Exception:
				raise ValueError("Your constructor function has an error in it.")

			
class TwoImageTransformation:

	def __init__(self, p, construct_class):
		super(TwoImageTransformation, self).__init__()
		self.p = p
		self.construct_class = construct_class

	def __call__(self, image1, image2):
		if image1 == None or image2 == None:
			raise ValueError("You have improperly called the image constructor.")
		else:
			if self.construct_class == None:
				raise ValueError("Constructor improperly called, please retry by properly applying a constructor for the transformation.")
			else:
				try:
					return self.construct_class(image1, image2)
				except Exception:
					raise ValueError("Your constructor function has an error in it.")		