import scipy.io
import numpy as np
import matplotlib.pyplot as plt

HS_file_name = "11-07-2021__16-13_90x45_integration_time=250000us"      #This is the file you want to analyze
#________________reading the mat file____________________________
mat = scipy.io.loadmat(f'{HS_file_name}.mat')
print(mat['mat'].shape)
wavelength = mat['wavelength']  #array 1X3648
img = mat['mat'] #matrix resY X resX X 3648
rev = mat['rev'] #matrix (resY*resX)X230X240X3
theta = mat['theta_list'] #matrix (resY*resX)X2

#________________Reconstructing a RGB image__________________
# for Flame VIS
R = 1951
G = 1386
B = 1083
print(img.max())
print(img.min())
resY = img.shape[0]
resX = img.shape[1]
rgb = np.zeros([resY, resX, 3])
rgb[:, :, 0] = img[:, :, R]
rgb[:, :, 1] = img[:, :, G]
rgb[:, :, 2] = img[:, :, B]

#________________Plotting the images_________________________
plt.figure()
plt.imshow(rgb / np.amax(rgb))
plt.show()
print('DONE!')