from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# img_ori = Image.open('./../../resources/edt_grids/EAC_256/edtplane_42.png')
# img_ori = Image.open('./../../edt_grids_RT147_256/TMJ_256/edtplane_42.png')
# img_ori = Image.open('./../../edt_grids_RT147_256/Sinus_+_Dura_256/edtplane_42.png')
img_ori = Image.open('./../../resources/edt_grids/sinus_1209_256/Segments1_256/edtplane_42.png')
img_new = Image.new("RGB", img_ori.size)
img_new.paste(img_ori) 
img = np.array(img_new)
print(img.shape)


img_new = Image.new("L", img_ori.size)
img_new = np.array(img_new)
print(img_new.shape)

for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        img_new[x][y] = img[x][y][0]



ax = plt.subplot()
im = ax.imshow(img_new)

# X = np.linspace(0,img_new.shape[0])
# Y = np.linspace(0,img_new.shape[1])

# im = ax.contourf(X, Y, img_new)
im = ax.contourf(img_new)
# create an Axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

plt.colorbar(im, cax=cax)
# plt.colorbar(im)

plt.show()
