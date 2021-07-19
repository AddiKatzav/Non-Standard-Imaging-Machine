import json
import time
import datetime
import subprocess
from socket import *
from flask_restful import Api
from flask import Flask, request, json, redirect
from flask_cors import cross_origin

app = Flask(__name__)
api = Api(app)
app_port = 4000


list_of_checkboxes = ['checkbox_all_sky_camera', 'checkbox_radiation_sensor', 'checkbox_gps']

default_client_inputs_dict = {
        "x_axis_resolution": -1, "y_axis_resolution": -1, "first_integration_time_micro_sec": -1,
        "second_integration_time_micro_sec": -1, "third_integration_time_micro_sec": -1,
        "delay_between_pixels_milisec": -1, "radiation_sensor_in_use": False, "gps_in_use": False,
        # "results_saving_directory": str(Path("Results"))}
        "results_saving_directory": ''}


def formatOutputFilename():
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    outputFilename = f"{value:%d-%m-%Y__%H-%M}"
    return outputFilename


def establish_app_connection():
    sock = socket()
    sock.bind(('localhost', app_port))
    sock.listen(1)
    app_socket = sock.accept()[0]
    return app_socket


def receive_post_data_from_client(default_client_inputs_dict):
    # Getting integration time, x and y axises resulotions from client:
    dict_res = default_client_inputs_dict
    dict_res["first_integration_time_micro_sec"] = int(request.form["first_integration_time_micro_sec"])
    dict_res["second_integration_time_micro_sec"] = int(request.form['second_integration_time_micro_sec'])
    dict_res["third_integration_time_micro_sec"] = int(request.form['third_integration_time_micro_sec'])
    dict_res["x_axis_resolution"] = int(request.form["x_axis_resolution"])
    dict_res["y_axis_resolution"] = int(request.form["y_axis_resolution"])
    dict_res["delay_between_pixels_milisec"] = int(request.form['delay_between_pixels_milisec'])
    dict_res["results_saving_directory"] = str(request.form["results_directory"]) + '\\' + formatOutputFilename()
    """______________________________________________________________________________________
    For future purposes we have here examples how to add the new sensors and HW devicds
    client_inputs_dict["radiation_sensor_in_use"] = request.form[]
    client_inputs_dict["gps_in_use"] = request.form[]
    _____________________________________________________________________________________"""
    return dict_res


def print_dictionary_key_value(dict_to_print):
    print([(key, dict_to_print[key]) for key in dict_to_print])


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():
    if request.method == 'GET':
        return redirect("http://localhost:3000")
    if request.method == 'POST':
        client_inputs_dict = receive_post_data_from_client(default_client_inputs_dict)
        """____________________________________________________________________
        If you are not connected to the HW use dummy_status_flag = True!"
        ____________________________________________________________________"""
        dummy_status_flag = True
        "_____________Mark true if you are using dummy status!______________"
        # If you are using dummy check as True
        # real_HW_devices_dict_ready_or_not = dummy_devices_dict_ready_or_not
        # Initializing the real_HW dict
        if dummy_status_flag:
            print("Notice! You are using dummy devices status\n")
            print("The user results_directory is " + str(client_inputs_dict["results_saving_directory"]))
        else:
            print("Using HW\n")
            proc = subprocess.Popen(["C:\\Anaconda3\\python.exe",
                                    "C:\\Users\\ora\\PycharmProjects\\HS_Scanner\\HS_Sampler_v1.3.1.py"])
            app_socket = establish_app_connection()
            parameters_str = json.dumps(client_inputs_dict)  # Turn parameters dict to string
            parameters_str += "\r\n\r\n"
            app_socket.send(parameters_str.encode())
        return redirect("http://localhost:3000")


if __name__ == '__main__':
    app.run(debug=True)

