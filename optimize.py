#!/usr/bin/env python2
from PIL import Image
from math import ceil
class PNGOptimize(object):

	image =	None
	def __init__(self, image):
		self.image = Image.open(image)

	def horizontal_fill(self, palette_position, nb_pixel = 3):
		"""
		Fill anything that is not the color of the given palette position
		for pixel between two pixel of color given by the palette_position.
		"""
		new_data = []
		width = self.image.size[0]
		color_index = -1
		non_color_count = 0
		for i,v in enumerate(self.image.getdata()):
			new_data.append(v)

			# starting a new line
			if i%width == 0: 
				color_index = -1
				non_color_count = 0
			if v == palette_position:
				if non_color_count != 0 and non_color_count < nb_pixel:
					for j in range(0, non_color_count):
						new_data[color_index+j+1] = palette_position
				color_index = i
				non_color_count = 0
			elif color_index != -1:
				non_color_count += 1
		self.image.putdata(new_data)

	def get_palette_position_by_usage(self, usage = 0, reverse = False):
		"""
		0 will give the most used color, 1 the second most used, etc.
		use reverse = True parameter so that 0 become the least used, 1 the second least used, etc.
		"""
		colors = sorted(self.image.getcolors(), key=lambda tup: tup[0], reverse=not(reverse))
		return colors[usage][1]

	def overwrite_palette(self, f):
		"""
		f is a function which receive the palette position. It must returns a list of three RGB value [0,0,0]
		"""
		new_palette = []
		for i in range(0, len(self.image.getpalette()), 3):
			values = f(i/3)
			if isinstance(values, list) and len(values) == 3:
				new_palette.append(values[0])
				new_palette.append(values[1])
				new_palette.append(values[2])
			else:
				new_palette += self.get_palette_rgb(i/3)
		self.image.putpalette(new_palette)

	def get_palette_rgb(self, position):
		"""
		returns a list of three value representing the RGB of the given position in the palette
		"""
		return self.image.getpalette()[position*3:position*3+3]

opt = PNGOptimize("image.png")
# First way
position = opt.get_palette_position_by_usage(0)
second_position = opt.get_palette_position_by_usage(1)
def overwrite(p):
	if p == position:
		return [0,0,0]
	else:
		return opt.get_palette_rgb(second_position)
opt.overwrite_palette(overwrite)
opt.horizontal_fill(position) # Fill anything that is between black pixel.
opt.image.show()
#second way
position = opt.get_palette_position_by_usage(1)
def overwrite(p):
	if p != position:
		return [0,0,0]
	else:
		return opt.get_palette_rgb(position)
opt.overwrite_palette(overwrite)
opt.horizontal_fill(position) # Fill anything that is between black pixel.
opt.image.show()
opt.image.save("captcha.png")
