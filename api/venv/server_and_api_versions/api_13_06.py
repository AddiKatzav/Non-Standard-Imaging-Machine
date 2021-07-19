""""
This is server_v7
Changes:
    #Try to operate the sytsem
    #Removing all yaml
    #Update button, sending HW status to the App.js
    #jsonify
"""

import os
import seabreeze as sb
import numpy as np
import serial
import cv2
import time
from pathlib import Path
from flask_restful import Resource, Api
import functools
from flask import Flask, make_response,render_template, request , flash ,json, redirect , jsonify
import time
import path_test




app = Flask(__name__)
api=Api(app)
results_saving_directory = Path("Results")



#results_saving_directory_string = str(results_saving_directory)

dummy_devices_dict_ready_or_not = {"gps_ready": True, "thermapp_TH_ready": False, "all_sky_camera_ready": True,
                                   "radiation_sensor_ready": False, "spectrometer": False, "review_camera": False,
                                   "arduino_controller": False}

default_client_inputs_dict = {
        "x_axis_resulotion": -1, "y_axis_resulotion":-1 , "integration_time_mili_sec": -1, "delay_between_pixels_milisec" :-1,
    "all_sky_camera_in_use": False, "radiation_sensor_in_use": False,
    "thermapp_TH_in_use": False,"gps_in_use": False,
    "results_saving_directory": str(Path("Results"))}


def receive_post_data_from_client(default_client_inputs_dict):
    # Initalizing the dictionary
    dict_res = default_client_inputs_dict
    # Assigning values from the client into the dictionary
    dict_res["integration_time_micro_sec"] = int(request.form['integration_time_micro_sec'])
    dict_res["x_axis_resulotion"] = int(request.form["x_axis_resulotion"])
    dict_res["y_axis_resulotion"] = int(request.form["y_axis_resulotion"])
    dict_res["delay_between_pixels_milisec"] = int(request.form['delay_between_pixels_milisec'])
    dict_res["results_saving_directory"] = str(request.form["results_directory"])
    """if request.form["Checkbox1"] == 'yes':
    client_inputs_dict["all_sky_camera_in_use"] = True
    if devices_dict_ready_or_not["all_sky_camera_ready"] == False:
        return ("One of the devices- All sky camera is not ready!")
    return ("All sky camera device is ready!")"""
    # client_inputs_dict["thermapp_TH_in_use"] = request.form[]
    # client_inputs_dict["radiation_sensor_in_use"] = request.form[]
    # client_inputs_dict["gps_in_use"] = request.form[]
    #print_dictionary_key_value(dict_res)
    return dict_res

list_of_checkboxes= ['checkbox_all_sky_camera' , 'checkbox_radiation_sensor' , 'checkbox_thermapp_TH', 'checkbox_gps']
#2F replace all Checkbox1 into checkboxes with names OR maybe just Checkbox1, Checkbox2 etc...


def print_dictionary_key_value(dict_to_print):
    print([(key, dict_to_print[key]) for key in dict_to_print])


def format_output_filename():
    timestamp=time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    outputFilename = f"{value:%d-%m-%Y__%H-%M}"
    return outputFilename


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
    implementation of inverse solution in differential steps
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
    '''
    a3 = -(a1 * np.sin(alpha2) * np.cos(dt) - a2 * np.cos(alpha2)) + np.sqrt(1 - n2**2 + (a1 * np.sin(alpha2) * np.cos(dt) - a2 * np.cos(alpha2))**2)
    K = a1 * np.cos(0) + a3 * np.sin(alpha2) * np.cos(dt)    # direction cosines
    L = a1 * np.sin(0) + a3 * np.sin(alpha2) * np.sin(dt)
    M = a2 - a3 * np.cos(alpha2)
    print 'dt =', np.degrees(dt), 'deg'
    '''
    return dt


def terminate():
    """ Closing the Spectrometer and the arduino CNC"""
    spec.close()
    grbl.close()


def create_HS_image_template():
    img = np.zeros([1, 1])  # HS image template

    rvw = []  # review image template

    resX = 40
    resY = 30
    # This is not the Field of view. The Field of view remains the same. It is
    point_list = []
    # 2F 09/01  X,Y need a
    X = np.linspace(-400., 400., num=resX, endpoint=True)  # for 90X680 ponts
    # 55:00 in the video
    # The maximum Field of view of the scanner is 6o degrees
    Y = np.linspace(405., 5., num=resY, endpoint=True)
    # X = np.linspace(-75., 75., num=resX, endpoint=True)  # for 40X30 ponts
    # Y = np.linspace(100., 25., num=resY, endpoint=True)
    """ The coordinate system is not axis-symmetric due to:
     The system is not cartesian , so the the movement -motion equations are more complicated
      The time of movement in the center is much longer rather then in the edges.
      2F 09/01 by I_K :
        Instead of O_A notation replace with:
        Field_Of_View = FOV
        a) Horizontal FOV (blue angle)
        b) Vertical FOV (red angle)
        *** Its not required in the GUI for the USER.
        """
    for y in Y:
        for x in X:
            point_list.append([x, y])

    # 2F 09/01 - Here 1:07:40 there are 2 functions for coordinates converting
    # XYZ2AE -
    # AE2PP -cartesian/cylinder to the 2 angles of the camera
    # Need to take it from loran/O_A
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
    start = time.time()
    for t in theta_list:
        print(str(1 + theta_list.index(t)) + ' out of ' + str(len(theta_list)))  # In which point we are scanning
        l = 'G0 X' + str(t[0]) + ' Y' + str(t[1])  # move
        # G0 is a move command
        # print(l)
        # grbl <-> serial
        grbl.write(str.encode(l + '\n'))
        # after you send coordinate you should get a reply whether the msg received or not
        # The indication is whether the command accepted NOT if the ACTION Happend.
        # There is no indication when it actually achieved the time.
        grbl_out = grbl.readline()
        # print(grbl_out.strip())

        """O_A Nowdays the natural delay of the system is enough.
        # Once the spectrometer returns value (pxl) the sample is done
        # The spectrometer delay is not controlable"""
        # p = 'G4 P' + str(0.5)                    # delay between each scanning point for lines.
        # ser.write(p + '\n')
        # print(p)
        # grbl_out = ser.readline()
        # print(grbl_out.strip())

        pxl = spec.intensities()  # sample - a line vector that holds the intensity of each wave-length
        # 2F place here another integration time iteration
        if img.all() == 0:  # If we are in the first pointing scan we just replace between them
            img = pxl
        else:  # Else - every other pixel we will append to the image data.
            img = np.append(img, pxl)
        # The resulted len of the image vector  is 3648* num of pixels
        # In the block below we take the data from the review,rvw, camera (RGB)
        # The location of each pixel is identical to the image from the rvw camera
        rval, a = cam.read()
        a = a[125:355, 205:445]  # This is the crop of the RGB camera

        # O_A now we are using camera with very large FOV and therefore, we keep only the parts of the image that is relevant
        rvw.append(a)
        # O_A here we go back to the "zero- point" when we finish the scan
    grbl.write(str.encode('X0.Y0.\n'))
    grbl_out = grbl.readline()
    print(grbl_out.strip())
    ### I have added the zoom-code of O_A the closing of the ports
    # O_A closing the ports is necessary in order to start a new scan
    end = time.time()
    print('Runtime: ' +str (end-start))
    grbl.close  # added by A_K
    spec.close()  # added by A_K
    # Disconnecting by hand the usb will enforce these two commands automatically.

    img = np.reshape(img, (resY, resX, resW))
    data = {'wavelength': spec.wavelengths(), 'mat': img, 'rev': rvw, 'int_time' :spec.integration_time_micros, 'theta_list': theta_list}
    savemat('HS_100621_', data)  # saves a matlab file 2F maybe to save it in another format also?
    terminate()

def get_HW_devices_status(HW_status_dict, client_inputs_dict):
    # ------------------ initiate Spectrometer communication------------------------ The first block
    """There are 3 devices : camera, spectrometer, and arduino
        If one of them is  failed to connect nogo =1 and then the scan will not started
        Parameters:
         1) nogo - a communication flag
         2) devices - holds all the spectrometers that connected to the PC

         2F 09/01 - by I_K
          1) Handling with another spectrometer devices[1], the optic fiber can handle with 2 spectrometer in series and not in parallel
          2)  The user should get an indication for the nogo, and the reason for the nogo error. """
    # 2F 10/04
    # Define new function and list of devices (add new ones such as GPS, radiation sensor)
    # Inform the client which device is connected and which is not
    print(100)
    nogo = 0

    sb_devices = sb.list_devices()  # sb.= SeaBreeze
    # print devices
    try:
        """------This is the initialization of the spectrometer---- """
        spectrometer = sb.Spectrometer(sb_devices[0])
        # we only have one spectrometer connected to the PC that's why we always take the first one
        spectrometer.integration_time_micros(client_inputs_dict["integration_time"])
        # The amount of time( in micro-sec) the the sensor is "alive" the longer it is it will produce a better signal with less noise
        # On a bright day we will choose 160~150msec
        # Inside the lab is 300msec
        # 2F 09/01 - this argument should be an input by the user , perhaps : user_integration_time
        resW = len(spectrometer.wavelengths())
    except IndexError:
        #print('No spectrometer found!!!')
        nogo = 1
        HW_status_dict["spectrometer"] = False
        #return{'No spectrometer found!!!'}
        return HW_status_dict
    # ------------------initiate review camera communication------------------------
    ## 2F 09/01 - I_K 1) Adding another SkyCamera via USB.

    """try:
        cam = cv2.VideoCapture(1)
        rval, a = cam.read()
        cam.set(15, -6.0)
    except IndexError:
        #print('No review camera found!!!')
        nogo = 1
        HW_status_dict["review_camera"] = False
        #return{'No review camera found!!!'}
        return HW_status_dict"""
    # ---------------------initiate Arduino communication---------------------------

    try:
        # The argument 115200 is the board rate - the communication rate of the arduino
        # - DO NOT CHANGE IT  - if you change it you must change also the code that burned on the ctrler itself.
        # 2F 09/01 making a constant 115200 - BOARD RATE
        """Adding to this arduino block by I_K:
        1) GPS
        2) Radiation Sensor
        O_A regarding to those components sequence:
        The Arduino now is configured as CNC controller and not An I/O controller.
        It is possible to configure it as I/O ctrler.
        Suggestion: ADDING ANOTHER ARDUINO to deal with I/O to GPS and Radiation Sensor.
        Nowdays the camera is connected to the computer with usb (The PC replaces the embedded ctrler within most of the cameras)
        -for grbl info go to cnc grbl firmware """
        grbl = serial.Serial('COM4', 115200)
        # If there is a problem with the arduino the first thing you should try check is the comport!
        grbl.write(str.encode('\r\n\r\n'))
        time.sleep(2)
        grbl.flushInput()
        grbl.write(str.encode('G21 G92X0Y0Z0\n'))
        """ G21 define the local coordinate system in the G-code (CNC Systems)
        G92X0Y0Z0 - This string tell the ctrler that The location of the engines is the origin - G9X2..  """
        grbl_out = grbl.readline()
        # print(grbl_out.strip())
    except IndexError:
        #print('No  Arduino controller found!!!')
        nogo = 1
        HW_status_dict["arduino_controller"] = False
        #return {'No  Arduino controller found!!!'}
        return HW_status_dict
    # -------------point list of scan pattern in cartesian coordinates--------------
    """ Variables:
        1) img  - holds the HyperSpectral Inforamtion Cube
        2) rvw  - holds the images of  RGB camera after the Beam splitter
        3) resX - Num of pixels to sample in X axis 
        4) resY - Num of pixels to sample in Y axis 
        point_list - holds the coordinates of each point we sample
        5) X- The Field of view 
        6) Y- The Field of view
        2F 09/01 by I_K:
        1) Let the resX/Y to be configured by the USER. 
        O_A - There is the minimal resulotion by the engines"""
    if (nogo == 0):
        #All devices are ok
        "___________This is the start of the scan, Assuming all components are OK"
        print('nogo is 0')
        create_HS_image_template()



"__________________________________________________________________"

def display_client_devices_ready(HW_devices_dict_ready_or_not):
    device_status_list= []
    for device in HW_devices_dict_ready_or_not:
        if device == False:
            return("One of the devices is not ready!")
    return("All devices are ready!")





client_inputs_fetched_flag = False  # 2F maybe unnecessary


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return redirect("http://localhost:3000")
    if request.method == 'POST':

        # Initializing the real_HW dict:
        #real_HW_devices_status= dummy_devices_dict_ready_or_not
        #if 'Update HW status' in request.form:
           HW_devices_status = get_HW_devices_status(HW_devices_status, client_inputs_dict)
           """print_dictionary_key_value(HW_devices_status)
           resp = jsonify(HW_devices_status)
           resp.status_code= 200 # 200 means its OK
           return resp
        elif 'Activate system' in request.form:
            global client_inputs_fetched_flag # 2F maybe unnecessary
            client_inputs_dict = receive_post_data_from_client(default_client_inputs_dict)

            ____________________________________________________________________
            If you are not connected to the HW use dummy_status_flag = True!
            ____________________________________________________________________"""
        dummy_status_flag = False
        "_____________Mark true if you are using dummy status!______________"

        if dummy_status_flag:
            print("Notice! You are using dummy devices status\n")
            print("The  user results_directory is "+ str(client_inputs_dict["results_saving_directory"]))
        else:
            print(200)
            get_HW_devices_status(dummy_devices_dict_ready_or_not, defclient_inputs_dict)

        print_dictionary_key_value(real_HW_devices_dict_ready_or_not)
        #return {'This is POST request on port 5000 ,The time is': date_and_time}
        return redirect("http://localhost:3000")
    #return {'This is NOT a GET or a POST request on port 5000 ,The time is': date_and_time}
    return redirect("http://localhost:3000")


@app.route('/hello')
def hello():
    return 'Hello, World!'





if __name__ == '__main__':
    app.run(debug=True)

