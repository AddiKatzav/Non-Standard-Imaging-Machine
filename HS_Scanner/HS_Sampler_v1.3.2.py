'''
HS sampler v1.3.1 with list of 3 integ time for each pixel

integration of scanning optics and spectrometer sampling
based on scanner_drive_v2.1 kinematics
* delays removed
* added usb camera capture
'''


import seabreeze.spectrometers as sb
from scipy.io import savemat
import numpy as np
import cv2
import serial
import time
from socket import *
import json

print("HS sampler - Starting to scan...")


def xyz2ae(x, y, z=1000.):
    '''
    conversion of cartesian coordinates
    :return: azimuth and elevation angles
    '''
    az = np.arctan2(y, x)
    el = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)
    # print 'azimuth =', np.degrees(az), 'elevation =', np.degrees(el), 'deg'
    return az, el

def ae2pp(az, el):
    '''
    Implementation of inverse solution in differential steps
    :param az:  azimuth angle
    :param el:  elevation angle
    :return: diff angle
    '''
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
    return dt


def terminate():
    spec.close()
    grbl.close()


# ------------------ initiate Server-Application communication------------------------
server_socket = socket()
server_port = 4000
server_socket.connect(('localhost', server_port))


# ------------------ Get GUI parameters ------------------------
NOT_RECEIVED_ALL = -1
parameters_str = ''
receiveStatus = NOT_RECEIVED_ALL
while receiveStatus == NOT_RECEIVED_ALL:
    parameters_str += server_socket.recv(1024).decode()
    receiveStatus = parameters_str.find("\r\n\r\n")  # Find end of message. If not found, continue receiving
parameters_str = parameters_str.lstrip("\r\n\r\n")  # Peel of end of message sign
client_inputs_dict = json.loads(parameters_str)  # Turn parameters_str to dictionary using JSON.
print(client_inputs_dict)
server_socket.close()

# ------------------ initiate Spectrometer communication------------------------

nogo = 0
integration_time_list = []
if client_inputs_dict["first_integration_time_micro_sec"] > 0:
    integration_time_list.append(client_inputs_dict["first_integration_time_micro_sec"])
if client_inputs_dict["second_integration_time_micro_sec"] > 0:
    integration_time_list.append(client_inputs_dict["second_integration_time_micro_sec"])
if client_inputs_dict["third_integration_time_micro_sec"] > 0:
    integration_time_list.append(client_inputs_dict["third_integration_time_micro_sec"])


empty_list_reference = []
img_list = []
data = []
rval_list = []
rvw_img = []


# Creating list of lists for initialization
for i in range(len(integration_time_list)):
    img_list.append(empty_list_reference)
    data.append(empty_list_reference)
    rval_list.append(empty_list_reference)
    rvw_img.append(empty_list_reference)



devices = sb.list_devices()

try:
    spec = sb.Spectrometer(devices[0])
    # resW is unique for each spectrometer,depending on nothing but the spec model (NIR/VIS)
    resW = len(spec.wavelengths())
    for i in range(len(integration_time_list)):
        spec.integration_time_micros(integration_time_list[i])

except IndexError:
    print('No spectrometer found!!!')
    nogo = 1

# ------------------initiate review camera communication------------------------

try:
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(cam)
    rval_list[0], rvw_img[0] = cam.read()
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

# -------------point list of scan pattern in cartesian coordinates--------------

if nogo == 0:
    for i in range(len(img_list)):
        img_list[i] = np.zeros([1, 1])  # HS image template
    rvw_list = []  # review image template
    resX = client_inputs_dict["x_axis_resolution"]
    resY = client_inputs_dict["y_axis_resolution"]
    point_list = []
    X = np.linspace(-400., 400., num=resX, endpoint=True)
    Y = np.linspace(405., 5., num=resY, endpoint=True)

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
    "Counting the total time of actual scanning process"
    start = time.time()
    for t in theta_list:
        l = 'G0 X' + str(t[0]) + ' Y' + str(t[1])  # move
        grbl.write(str.encode(l + '\n'))
        grbl_out = grbl.readline()
        if theta_list.index(t) % resX == 0:
            p = 'G4 P' + str(0.5)  # delay
            grbl.write(str.encode(p + '\n'))
            grbl_out = grbl.readline()

        for i in range(len(integration_time_list)):
            print('Image number ' + str(i) + ' sample number :' + str(1 + theta_list.index(t)) + ' out of ' + str(
                len(theta_list)))
            pxl = spec.intensities()  # sample is taken here
            if img_list[i].all() == 0:
                img_list[i] = pxl
            else:
                img_list[i] = np.append(img_list[i], pxl)
            rval_list[i], rvw_img[i] = cam.read()
            rvw_img[i] = rvw_img[i][125:355, 205:445]
            rvw_list.append(rvw_img[i])
    grbl.write(str.encode('X0.Y0.\n'))
    grbl_out = grbl.readline()
    print(grbl_out.strip())
    end = time.time()
    print('Runtime: ' + str(end - start))
    for i in range(len(integration_time_list)):
        img = img_list[i]
        img = np.reshape(img, (resY, resX, resW))
        spec.integration_time_micros(integration_time_list[i])
        data[i] = {'wavelength': resW, 'mat': img, 'rev': rvw_list[i], 'int_time': integration_time_list[i],
                'theta_list': theta_list}
        integ_time_us = int(integration_time_list[i])
        file_name = f'{client_inputs_dict["results_saving_directory"]}_integration_time={integ_time_us}us'
        savemat(file_name, data[i])

terminate()

cv2.destroyAllWindows()


print("Scan finished successfully")
