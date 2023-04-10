from PIL import Image
import numpy as np


img = Image.open('../../../edtplane_155.png')
img_new = Image.new("RGB", img.size)
img_new.paste(img) 
img = np.array(img_new)
print(img.shape)

print(img[0][0])
print(img[100][100])
print(img[0][0])

for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        if(img[x][y][0] == 1 and img[x][y][2] < 10 ):
            img[x][y] = [0, 255, 0]
        else:
            img[x][y] = [0, 0, 0]

Image.fromarray(img).save('../../../test.png')