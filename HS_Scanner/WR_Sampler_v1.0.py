'''
integration of scanning optics and spectrometer sampling for sampling 9 point
white refference cube using Spectralon on a tripod. breakes were added to allow
the operator to reposition the spectralon.
based on scanner_drive_v2.1 kinematics

field experiment at 30.1.19 at Gilat
field experiment at 26.3.19 at ARO
field experiment at 28.3.19 at ARO
field experiment at 8.4.19 at Gilat
'''

import numpy as np
import serial
import time
import seabreeze.spectrometers as sb
from scipy.io import savemat
import cv2
import matplotlib.pyplot as plt


# ------------------------conversion to azimuth-elevation-----------------------
def xyz2ae(x, y, z=1000.):
    az = np.arctan2(y, x)
    el = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)
    # print 'azimuth =', np.degrees(az), 'elevation =', np.degrees(el), 'deg'
    return az, el


# ----------------------------- inverse solution--------------------------------

def ae2pp(az, el):
    alpha1 = np.radians(25.0)  # prism deviation angles
    alpha2 = np.radians(25.0)
    n1 = 1.5  # prism index of refraction
    n2 = 1.5
    # coefficients for configuration 2112 in group A
    a1 = np.sin(alpha1) * (np.cos(alpha1) - np.sqrt(n1 ** 2 - np.sin(alpha1) ** 2))
    a2 = -np.sqrt(
        n2 ** 2 - n1 ** 2 + (np.sin(alpha1) ** 2 + np.cos(alpha1) * np.sqrt(n1 ** 2 - np.sin(alpha1) ** 2)) ** 2)
    p1 = (a1 * np.tan(alpha2)) ** -1
    p2 = (2 * (a2 + np.cos(el))) ** -1
    p3 = ((a2 + np.cos(el)) ** 2) * np.cos(alpha2) ** -2
    dt = np.pi - np.arccos(p1 * (a2 + p2 * (1 - n2 ** 2 - p3)))
    # a3 = -(a1 * np.sin(alpha2) * np.cos(dt) - a2 * np.cos(alpha2)) + np.sqrt(1 - n2**2 + (a1 * np.sin(alpha2) * np.cos(dt) - a2 * np.cos(alpha2))**2)
    # K = a1 * np.cos(0) + a3 * np.sin(alpha2) * np.cos(dt)    # direction cosines
    # L = a1 * np.sin(0) + a3 * np.sin(alpha2) * np.sin(dt)
    # M = a2 - a3 * np.cos(alpha2)
    # print 'dt =', np.degrees(dt), 'deg'
    return dt


def terminate():
    spec.close()
    grbl.close()


# ------------------ initiate Spectrometer communication------------------------

nogo = 0
integ_time = 300*1000
devices = sb.list_devices()
print(devices)
try:
    spec = sb.Spectrometer(devices[0])
    spec.integration_time_micros(integ_time)
    resW = len(spec.wavelengths())
except:
    print('No spectrometer found!!!')
    nogo = 1

# img = np.zeros([1, 1]) # HS image template
# ------------------initiate review camera communication------------------------

try:
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    rval, a = cam.read()
    cam.set(15, -6.0)
except IndexError:
    print('No review camera found!!!')
    nogo = 1

# ---------------------initiate Arduino communication---------------------------
try:
    grbl = serial.Serial('COM5', 115200)
    grbl.write(str.encode('\r\n\r\n'))
    time.sleep(2)
    grbl.flushInput()
    grbl.write(str.encode('G21 G92X0Y0Z0\n'))
    grbl_out = grbl.readline()
    # print(grbl_out.strip())
except IndexError:
    print('No controller found!!!')
    nogo = 1
# -------------point list of scan pattern in cartesian coorditates--------------
if nogo == 0:
    img = np.zeros([1, 1])  # HS image template
    rvw = []  # review image template

    resX = 90
    resY = 45

    point_list = []
    X = np.linspace(-400., 400., num=resX, endpoint=True)  # for 90X68 ponts
    Y = np.linspace(405., 5., num=resY, endpoint=True)
    # X = np.linspace(-75., 75., num=resX, endpoint=True)  # for 40X30 ponts
    # Y = np.linspace(100., 25., num=resY, endpoint=True)
    for y in Y:
        for x in X:
            point_list.append([x, y])

    # ---------------------------create position list-------------------------------

    theta_list = []
    theta1 = 0.
    theta2 = 0.
    tmp_az = 0.
    tmp_dt = 0.
    for X in point_list:
        az, el = xyz2ae(X[0], X[1])
        dt = ae2pp(az, el)
        theta1 = theta1 + 0.5 * (dt - tmp_dt) + az - tmp_az
        theta2 = theta2 - 0.5 * (dt - tmp_dt) + az - tmp_az
        tmp_az = az
        tmp_dt = dt
        theta_list.append([theta1, theta2])
    # ---------------------------loop thru positions--------------------------------

    for t in theta_list:
        print(str(1 + theta_list.index(t)) + ' ot of ' + str(len(theta_list)))
        l = 'G0 X' + str(t[0]) + ' Y' + str(t[1])
        # print(l)
        grbl.write(str.encode(l + '\n'))
        grbl_out = grbl.readline()
        # print(grbl_out.strip())
        if theta_list.index(t) % resX == 0:
            p = 'G4 P' + str(0.5)  # delay
            # print(p)
            grbl.write(str.encode(p + '\n'))
            grbl_out = grbl.readline()
            # print(grbl_out.strip())

        pxl = spec.intensities()
        if img.all() == 0:
            img = pxl
        else:
            img = np.append(img, pxl)

        rval, a = cam.read()
        a = a[125:355, 205:445]
        rvw.append(a)

    grbl.write(str.encode('X0.Y0.\n'))
    grbl_out = grbl.readline()
    print(grbl_out.strip())

    img = np.reshape(img, (resY, resX, resW))
    data = {'wavelength': spec.wavelengths(), 'mat': img, 'rev': rvw, 'int_time': spec.integration_time_micros,
            'theta_list': theta_list}
    integ_time = int(integ_time/1000)
    savemat(f'WR100721_{resY}x{resX}_{integ_time}ms_3_VIS', data)

terminate()

# for Flame VIS
R = 1951
G = 1386
B = 1083

# %% ----------reconstruct RGB image (non calibrated data)--------------------
rgb = np.zeros([resY, resX, 3])
rgb[:, :, 0] = img[:, :, R]
rgb[:, :, 1] = img[:, :, G]
rgb[:, :, 2] = img[:, :, B]
plt.figure()
plt.imshow(rgb / np.amax(rgb))
plt.show()

# %%
plt.figure()
plt.plot(spec.wavelengths(), img[0, 0, :])
plt.plot(spec.wavelengths(), img[1, 1, :])


# ------added for cv2.VideoCapture so a certain error wouldnt pop up------
cv2.destroyAllWindows()