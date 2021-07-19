//This is v1, in this we added saving configuration data into json file
import React, { Component } from 'react';
import './style.css';
//import {useState} from 'react';
import configData from './data_config.json';
import ValidationForm from './ValidationForm'; // Based on : https://www.youtube.com/watch?v=FM2RN8rHCTE
//const fs = require("fs");
//const path = require("path");
var FileSaver = require('file-saver');
//const configDirectory = 'C:\\Users\\Dell\\Desktop\\Final_Project\\Flask_React_Merged\\ScanConfigs\\';

const fetchData = () => {
return fetch("http://127.0.0.1:5000/")
      .then((response) => response.json())
      .then((data) => console.log(data));}


function validateForm() {
  let resX = document.forms["main_form"]["x_axis_resolution"].value;
  let resY_test = document.forms["main_form"]["y_axis_resolution"].value;
  let resY = document.forms["main_form"]["y_axis_resolution"].value;
  let fovX = document.forms["main_form"]["FOV_X"].value;
  let fovY = document.forms["main_form"]["FOV_Y"].value;
  let fov_i = 1.2;
  let integration_time_1 = document.forms["main_form"]["first_integration_time_micro_sec"].value;
  let integration_time_2 = document.forms["main_form"]["second_integration_time_micro_sec"].value;
  let integration_time_3 = document.forms["main_form"]["third_integration_time_micro_sec"].value;
  let max_integration_time = 65*1000000; //max value is 65 second
  let min_integration_time = 1*1000; // min value is 1 milisecond
  let valid_to_submit = true;
  if (resY_test==55) {
	  alert("you put 55");
	  valid_to_submit = false;
	  return false;
  };
  
  if (resX < (fovX /fov_i)) {
    alert("X axis resolution must be bigger!");
	valid_to_submit = false;
    return false; 
  };
  if (resY < (fovY /fov_i)) {
    alert("Y axis resolution must be bigger!");
	valid_to_submit = false;
    return false;
  };
  if (resX*fovY != resY*fovX) {
    alert("FOV ratio must be as Resolution ratio!");
	valid_to_submit = false;
    return false;
  };
  if (integration_time_1 <min_integration_time  || integration_time_1 >max_integration_time){
    alert("Integration time is out of range!");
	valid_to_submit = false;
    return false;
  };
  if (integration_time_2 <min_integration_time  || integration_time_2 >max_integration_time){
    alert("Integration time is out of range!");
	valid_to_submit = false;
    return false;
  };
  if (integration_time_3 <min_integration_time  || integration_time_3 >max_integration_time){
    alert("Integration time is out of range!");
	valid_to_submit = false;
    return false;
  };
  if (valid_to_submit==true){
	document.getElementById("main_form").submit();
	return(true);
  }else{
	  return(false);
  }

}
  



function loadFile() {
  return new Promise((resolve,reject)=> {
	  

    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
      alert("The file API isn't supported on this browser yet.");
      return;
    }

    input = document.getElementById('fileInput');
    if (!input) {
      alert("Um, couldn't find the fileinput element.");
    }
	
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");
    }
    else {
      file = input.files[0];
      fr = new FileReader();
      fr.onload = receivedText;
      fr.readAsText(file);
    }

    function receivedText(e) {
      let lines = e.target.result;
      var newArr = JSON.parse(lines);
	  //return newArr;
	  console.log(newArr.text_box);
	  var newState ={
		    first_integration_time: newArr.text_box.first_integration_time_micro_sec, //configData.integration_time_micro_sec,
			second_integration_time: newArr.text_box.second_integration_time_micro_sec,
			third_integration_time: newArr.text_box.third_integration_time_micro_sec,
			x_axis_resolution: newArr.text_box.x_axis_resolution,
			y_axis_resolution: newArr.text_box.y_axis_resolution,
			delay_between_pixels_milisec: newArr.text_box.delay_between_pixels_milisec,
			results_directory: newArr.text_box.results_directory,
			config_file_name: ""
	  }
	  resolve(newState);
    }
  });
  } 

class App extends Component {
	
  state = {
    first_integration_time:configData.text_box.first_integration_time_micro_sec,//configData.integration_time_micro_sec,
	second_integration_time:configData.text_box.second_integration_time_micro_sec,
	third_integration_time:configData.text_box.third_integration_time_micro_sec,
	x_axis_resolution: configData.text_box.x_axis_resolution,
	y_axis_resolution:configData.text_box.y_axis_resolution,
	FOV_X:configData.text_box.FOV_X,
	FOV_Y:configData.text_box.FOV_Y,
	delay_between_pixels_milisec: configData.text_box.delay_between_pixels_milisec,
	results_directory: configData.text_box.results_directory,
	config_file_name: ""

	
	
	
  }

	handleFirstIntegrationTimeInput = e => {
		this.setState({first_integration_time: e.target.value.toLocaleString()});
	};
	handleSecondIntegrationTimeInput = e => {
		this.setState({second_integration_time: e.target.value});
	};
	handleThirdIntegrationTimeInput = e => {
		this.setState({third_integration_time: e.target.value});
	};
	handleXAxisResolution = e =>{
		this.setState({x_axis_resolution: e.target.value});
	};
	handleFOV_X = e =>{
		this.setState({FOV_X: e.target.value});
	};
	handleFOV_Y = e =>{
		this.setState({FOV_Y: e.target.value});
	};
	handleYAxisResolution = e =>{
		this.setState({y_axis_resolution: e.target.value});
	};
	handleDelayBetweenPixels = e =>{
		this.setState({delay_between_pixels_milisec: e.target.value});
	};
	handleResultsDirectory = e =>{
		this.setState({results_directory: e.target.value});
	};
	handleConfigName = e =>{
		this.setState({config_file_name: e.target.value});
	};
	handleLoadConfigFile = async (e) =>{
		const newState = await loadFile();
		this.setState(newState, () => {});
	}; 

	handleSaveConfigFile = e =>{
		const newConfigDataObject= {
			text_box: {
				results_directory: this.state.results_directory,
				first_integration_time_micro_sec: this.state.first_integration_time,
				second_integration_time_micro_sec: this.state.second_integration_time,
				third_integration_time_micro_sec: this.state.third_integration_time,
				x_axis_resolution: this.state.x_axis_resolution,
				y_axis_resolution: this.state.y_axis_resolution,
				FOV_X: this.state.FOV_X,
				FOV_Y: this.state.FOV_Y,
				delay_between_pixels_milisec: this.state.delay_between_pixels_milisec
			}
		};
		const jsonConfigData = JSON.stringify(newConfigDataObject);
		//var pathhh = configDirectory;
		var file_name = this.state.config_file_name;
		var file_name_json = file_name.concat('.json');
		var blob= new Blob([jsonConfigData],{type : 'application/json'});
		FileSaver.saveAs(blob,file_name.concat(".json"));
	};

	handleSubmit(event){
	//let resX = document.forms["main_form"]["x_axis_resolution"].value;
	//var resY_text = this.state.y_axis_resolution;
	//let resY = document.forms["main_form"]["y_axis_resolution"].value;
	//let fovX = document.forms["main_form"]["FOV_X"].value;
	//let fovY = document.forms["main_form"]["FOV_Y"].value;
	//let fov_i = 1.2;
	//let integration_time_1 = document.forms["main_form"]["first_integration_time_micro_sec"].value;
	//let integration_time_2 = document.forms["main_form"]["second_integration_time_micro_sec"].value;
	//let integration_time_3 = document.forms["main_form"]["third_integration_time_micro_sec"].value;
	//let max_integration_time = 65*1000000; //max value is 65 second
	//let min_integration_time = 1*1000; // min value is 1 milisecond
	//if (resY_text==55) {
	alert("you put "+ this.state.y_axis_resolution.value);
	event.preventDefault();
	}
	
  //WORK UNTIL HERE
  render(){
  return (
    <div className="App">
	<ValidationForm/>
    </div>
  );
  }
}

export default App;
