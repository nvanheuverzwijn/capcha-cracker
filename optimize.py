#!/usr/bin/env python2
from PIL import Image
from captcha import Captcha
import os

opt = Captcha("image.png")
# First way
position = opt.get_palette_position_by_usage(0)
second_position = opt.get_palette_position_by_usage(1)
def overwrite(p):
	if p == position:
		return [8,8,8]
	else:
		return opt.get_palette_rgb(second_position)
opt.overwrite_palette(overwrite)
opt.horizontal_fill(position) # Fill anything that is between black pixel.
#second way
position = opt.get_palette_position_by_usage(1)
def overwrite(p):
	if p != position:
		return [0,0,0]
	else:
		return [255,255,255]
opt.overwrite_palette(overwrite)
opt.horizontal_fill(position) # Fill anything that is between black pixel.
opt.image.save("captcha.png")
opt.image.show()
print opt.image.getpalette()
letters = opt.extract_letters([1])

os.mkdir("letters")
letters[0].save("letters/letter0.png")
letters[1].save("letters/letter1.png")
letters[2].save("letters/letter2.png")
letters[3].save("letters/letter3.png")
