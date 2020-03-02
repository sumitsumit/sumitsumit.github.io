import os, path, sys
from PIL import Image

image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
thumbnail_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'thumbnails'))
THUMBNAIL_WIDTH = 400

for filename in os.listdir(image_path):
    print(filename)
    input_file = os.path.join(image_path,filename)
    output_file = os.path.join(thumbnail_path,filename)
    im = Image.open(input_file)
    scale_factor = THUMBNAIL_WIDTH/float(im.size[0])
    thumb_size = (int(im.size[0]*scale_factor), int(im.size[1]*scale_factor))
    im.thumbnail(thumb_size, Image.ANTIALIAS)
    im.save(output_file, 'JPEG')



