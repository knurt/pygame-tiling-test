class Animationframe:
	
	def __init__(self, image, rect, duration, offset):
		"""
		image: of the type 'surface'
		rect: rectangle defining the section of the image displayed
		duration: how many frames the animationstate lasts
		offset: x/y-tuple, defines offset
		"""
		self.image = image
		self.rect = rect
		self.duration = duration
		self.offset = offset

		
