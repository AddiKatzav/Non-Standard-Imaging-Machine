//This is v1, in this we added saving configuration data into json file
import React, { Component } from 'react';
import './style.css';
//import {useState} from 'react';
import configData from './data_config.json';
//const fs = require("fs");
//const path = require("path");
var FileSaver = require('file-saver');
//const configDirectory = 'C:\\Users\\Dell\\Desktop\\Final_Project\\Flask_React_Merged\\ScanConfigs\\';

const fetchData = () => {
return fetch("http://127.0.0.1:5000/")
      .then((response) => response.json())
      .then((data) => console.log(data));}



  



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
		this.setState({first_integration_time: e.target.value});
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
    <body>
<form name= "main_form" id="main_form" action="" onSubmit={this.handleSubmit} method="post">
<table style={{width: "100%"}}>
	<tr>
		<th className="auto-style1" colSpan="3">  <center>Welcome</center></th>
	</tr>
	<tr>
		<td >

			<input checked="checked" name="Radio1" type="radio" />Hyper Spectral
			Scan<br />
			<input name="Radio1" type="radio" />WR - White Target Scan
		</td>
		<td 
		className="auto-style1"><center>Choose Configuration </center>
			
			<input name="loadedConfigFile" id = 'fileInput' type="file"/>
		
		</td>
		<td className="auto-style1">Load configuration from file
			<tr> <input 
			name= "loadConfigButton"
			type= "button"
			id = "buttonLoad"
			value= "Load"
			onClick={this.handleLoadConfigFile}/>  </tr>
			
		</td>
	</tr>
		<tr>
		<td>
		&nbsp;
		</td>
		
			<td className="auto-style1"><strong><center>Add units to scan</center></strong><table style={{width: "100%"}}>
			<tr>
				<td>Unit</td>
				<td>Status</td>
				<td>Add</td>
			</tr>

			<tr>
				<td>Radiation sensor</td>
				<td>&nbsp;</td>
				<td><input name="Checkbox2" type="checkbox" /></td>
			</tr>

			<tr>
				<td>GPS</td>
				<td>&nbsp;</td>
				<td><input name="Checkbox4" type="checkbox" /></td>
			</tr>

		</table>
		</td>
		<td>
		&nbsp;
		</td>
	</tr>
	
	<tr>
		<td style={{width: "280px"}}>
		Enter <strong>first</strong> integration time [<strong>μ</strong>Sec]<br />
		<input 
			name ="first_integration_time_micro_sec"
			type="text"
			required
			onChange={this.handleFirstIntegrationTimeInput}	
			value={this.state.first_integration_time}/><br />
		</td>
		<td>
		&nbsp;
		</td>
		
		<td>
		Choose X axis resolution<br/>
		<input
			name="x_axis_resolution"
			type="text"
			required
			onChange={this.handleXAxisResolution}	
			value={this.state.x_axis_resolution}/><br />
		
		</td>

	</tr>
	<tr>
		<td>
		Enter  <strong>second</strong> integration time [<strong>μ</strong>Sec]<br />
		<input 
			name ="second_integration_time_micro_sec"
			type="text"
			required
			onChange={this.handleSecondIntegrationTimeInput}	
			value={this.state.second_integration_time}/><br />
		</td>
		<td>
		&nbsp;
		</td>
		<td >Choose Y axis resolution<br/>
			<input 
			name="y_axis_resolution"
			required
			type="text"
			onChange={this.handleYAxisResolution}	
			value={this.state.y_axis_resolution}/><br />
		</td>
	</tr>
	<tr>
		<td>
		Enter <strong>third</strong> integration time [<strong>μ</strong>Sec]<br />
		<input 
			name ="third_integration_time_micro_sec"
			type="text"
			required
			onChange={this.handleThirdIntegrationTimeInput}	
			value={this.state.third_integration_time}/><br />
		</td>
		<td>
		&nbsp;
		</td>
		<td>
		Enter FOV in X axis [°]<br/>
			<input 
			name ="FOV_X"
			type="text"
			required
			onChange={this.handleFOV_X}	
			value={this.state.FOV_X}/><br />

		</td>
	</tr>
	<tr>
		<td >Delay between pixels [<strong>m</strong>Sec] <br />
		<input 
			name="delay_between_pixels_milisec" 
			type="text"
			onChange={this.handleDelayBetweenPixels}	
			value={this.state.delay_between_pixels_milisec}/>
		</td>
		<td>
		&nbsp;
		</td>
		<td>
		Enter FOV in Y axis [°]<br/>	
			<input 
			name ="FOV_Y"
			type="text"
			required
			onChange={this.handleFOV_Y}	
			value={this.state.FOV_Y}/><br />
		</td>
	
	</tr>

	<tr>
		<td>Configuration file name:
			<tr> 
			<input
			name ="config_file_name"
			type="text"
			placeholder ="Your File Name"
			onChange={this.handleConfigName}	
			value={this.state.config_file_name}
			/>
			<br />
			</tr>
		Save Configuration
		<tr>
		<input 
			name="save_config_button"
			type="button" 
			value="Save"
			onClick={this.handleSaveConfigFile}
			/>

		</tr>

		</td>
		<td rowspan="2">
			<center> 
			<div className="auto-style1">
				<br />
				<button 
				name="submit_activate"
				//onclick= "validateFrom();"
				style={{ backgroundColor: "Green" , width: "120px" , height: "60px", fontWeight: "bold", fontSize:14}} 
				type="submit" value="Activate" /><br />
			</div>
			
		<div className="auto-style1">
			Check devices state</div>
			<div className="auto-style1">
				<input name="Submit2" style={{backgroundColor: "Yellow"}} type="submit" value="Check State" />
				</div>
				</center>
		</td>
		<td style={{height: "119px"}}>Save scan results to:<br />
		<input 
			name="results_directory"
			
			type="text"
			onChange={this.handleResultsDirectory}	
			value={this.state.results_directory}/>
		</td>
	</tr>
	<tr>

	</tr>
</table>
 
			
			{/*}  <p>{this.state.first_integration_time}</p>
 <p>{this.state.second_integration_time}</p>
 <p>{this.state.y_axis_resolution}</p>
  <p>{this.state.config_file_name}</p>  */}
</form>
</body>




    </div>
  );
  }
}

export default App;
