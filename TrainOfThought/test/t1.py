from PIL import Image

# import pygame
# pygame.init()

DIR = '../Images\\'

FILE_NAMES = (
	'UBB.bmp', 'UWW.bmp', 'URR.bmp', 'UYY.bmp',
	'UOO.bmp', 'UGG.bmp', 'UPP.bmp', 'ULL.bmp', 
	'DBB.bmp', 'DWW.bmp', 'DRR.bmp', 'DYY.bmp',
	'DOO.bmp', 'DGG.bmp', 'DPP.bmp', 'DLL.bmp', 
	'RBB.bmp', 'RWW.bmp', 'RRR.bmp', 'RYY.bmp',
	'ROO.bmp', 'RGG.bmp', 'RPP.bmp', 'RLL.bmp', 
	'LBB.bmp', 'LWW.bmp', 'LRR.bmp', 'LYY.bmp',
	'LOO.bmp', 'LGG.bmp', 'LPP.bmp', 'LLL.bmp', 
)

# bmp = pygame.image.load(DIR + 'UBB.bmp')
# bmpa = pygame.image.tobytes(bmp, pygame.ARGB)
# print(bmpa)

  
img = Image.open(DIR + 'UBB.bmp')
image.save()
  
