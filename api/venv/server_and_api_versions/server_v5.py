""""
Here we changed:
Added reading the config.yaml file
Changed redirections : always redirect to localhost:3000
if you go to localhost:5000/time you will see the time and date
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
from flask import Flask, make_response,render_template, request , flash ,json, redirect
import time
import yaml
import path_test


current_path = Path().absolute()    #The current application path
config_yaml_file = "basic_cfg.yml"

app = Flask(__name__)
api=Api(app)

base_page = "base_7.html"
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



def load_config_arguments(default_client_inputs_dict, current_path, config_yaml_file,):
    # Loading the whole configuration from a file
    client_input_dict_load_from_config = default_client_inputs_dict
    path_config_file = getPathScanConfigFile(current_path, config_yaml_file)
    config_yaml_file = open(path_config_file, "r")
    # DONT FORGET TO CLOSE config_yaml_file!!!
    parsed_config_yaml_file = yaml.load(config_yaml_file, Loader=yaml.FullLoader)
    client_input_dict_load_from_config
    config_yaml_file.close()
    return client_input_dict_load_from_config
#client_input_dict_load_from_config = load_config_arguments(default_client_inputs_dict, config_file)

def receive_post_data_from_client(default_client_inputs_dict):
    # Getting integration time, x and y axises resulotions from client:
    dict_res = default_client_inputs_dict
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

def get_date_and_time():
    timestamp=time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    date_and_time = f"{value:%Y-%m-%d %H:%M:%S}"
    return date_and_time

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
def get_HW_devices_status(real_HW_devices_dict_ready_or_not,client_inputs_dict):
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
        print('No spectrometer found!!!')
        nogo = 1
        real_HW_devices_dict_ready_or_not["spectrometer"] = False
    # ------------------initiate review camera communication------------------------
    ## 2F 09/01 - I_K 1) Adding another SkyCamera via USB.

    try:
        cam = cv2.VideoCapture(1)
        rval, a = cam.read()
        cam.set(15, -10.0)
    except IndexError:
        print('No review camera found!!!')
        nogo = 1
        real_HW_devices_dict_ready_or_not["review_camera"] = False
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
        print('No controller found!!!')
        nogo = 1
        real_HW_devices_dict_ready_or_not["arduino_controller"] = False
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
        create_HS_image_template()



"__________________________________________________________________"

def display_client_devices_ready(HW_devices_dict_ready_or_not):
    device_status_list= []
    for device in HW_devices_dict_ready_or_not:
        if device == False:
            return("One of the devices is not ready!")
    return("All devices are ready!")


client_inputs_fetched_flag = False  # 2F maybe unnecessary
@app.route("/", methods=["GET", "post"])
def index():
    if request.method == 'GET':
        return redirect("http://localhost:3000")
    if request.method == 'POST': #THIS IS CASE SENSATIVE
        global client_inputs_fetched_flag # 2F maybe unnecessary
        client_inputs_dict = receive_post_data_from_client(default_client_inputs_dict)

        """____________________________________________________________________
        If you are not connected to the HW use dummy_status_flag = True!"
        ____________________________________________________________________"""
        dummy_status_flag = True
        "_____________Mark true if you are using dummy status!______________"
        # If you are using dummy check as True
        real_HW_devices_dict_ready_or_not = dummy_devices_dict_ready_or_not
        # Initializing the real_HW dict
        if dummy_status_flag:
            print("Notice! You are using dummy devices status\n")
            print("The  user results_directory is "+ str(client_inputs_dict["results_saving_directory"]))
        else:
            get_HW_devices_status(real_HW_devices_dict_ready_or_not, client_inputs_dict)

        print_dictionary_key_value(real_HW_devices_dict_ready_or_not)
        #return {'This is POST request on port 5000 ,The time is': date_and_time}
        return redirect("http://localhost:3000")
    #return {'This is NOT a GET or a POST request on port 5000 ,The time is': date_and_time}
    return redirect("http://localhost:3000")


@app.route('/hello')
def hello():
    return 'Hello, World!'



@app.route('/time')
def get_current_time():
    date_and_time =get_date_and_time()
    return {'The time is': date_and_time}


if __name__ == '__main__':
    app.run(debug=True)

