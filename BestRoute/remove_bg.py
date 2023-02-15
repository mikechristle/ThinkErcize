# ---------------------------------------------------------------------------
# Remove Background
# Mike Christle 2022
#
# Reads in a .bmp file, replaces all white pixels with transparency,
# then writes the image to a .png file.
# ---------------------------------------------------------------------------

from PIL import Image
from glob import glob

BG_COLOR = 255, 255, 255

for file in glob(r'Images\car.bmp'):
    print(file)
    file1 = file[:-3] + 'png'
    img0 = Image.open(file)
    img0.save(file1, 'PNG', transparency=BG_COLOR)
