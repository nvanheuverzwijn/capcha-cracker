#!/usr/bin/env python

import requests
import sys
import time
import subprocess
from PIL import Image
from math import ceil
#import PIL from Image
#import ImageEnhance

tmp = 'image.png'
url = 'http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3'
signin= url + '/signin'
chal = url + '/challenge'
image= url + '/image'
logout= url + '/?logout=1'


c=requests.session()
c.get(signin)
data = dict(username='rock', password='rock', fuel_csrf_token=c.cookies['fuel_csrf_token'])
r = c.post(signin, data=data)

for i in range(0,500):
    c.get(chal)
    png = c.get(image)
    t = open(tmp,'w')
    t.write(png.content)
    t.close()

    time.sleep(0.1)

    im = Image.open("image.png")
    palette = im.getpalette()
    colors = sorted(im.getcolors(), key=lambda tup: tup[0], reverse=True)
    position = colors[1][1]
    rgb = palette[position*3:(position*3+3)]
    new_palette = []
    for i,v in enumerate(palette):
            if ceil((int(i))/3) != position:
                    new_palette.append(0)
            else:
                    new_palette.append(palette[i])
    im.putpalette(new_palette)

    new_data = []
    lastpos = 0
    for i,v in enumerate(im.getdata()):
            new_data.append(v)
            if v == position:
                    new_data[lastpos] = v
            lastpos = i
    im.putdata(new_data)
    im.save("optimized.png")

    caca = subprocess.check_output('tesseract optimized.png stdout', shell=True)
    print caca.replace('®', '0')

c.get(logout)
