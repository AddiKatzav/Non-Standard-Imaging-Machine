//This is v1, in this we added saving configuration data into json file
import React, { Component } from 'react';
import './style.css';
import {useState} from 'react';
import configData from './data_config.json';
const fs = require("fs");
const path = require("path");
var FileSaver = require('file-saver');
const configDirectory = 'C:\\Users\\Dell\\Desktop\\Final_Project\\Flask_React_Merged\\ScanConfigs\\';


 

class App extends Component {
	
  state = {
    integration_time:configData.text_box.integration_time_micro_sec,//configData.integration_time_micro_sec,
	x_axis_resulotion: configData.text_box.x_axis_resulotion,
	y_axis_resulotion:configData.text_box.y_axis_resulotion,
	delay_between_pixels_milisec: configData.text_box.delay_between_pixels_milisec,
	results_directory: configData.text_box.results_directory,
	config_file_name: ""

	
	
	
  }

	handleIntegrationTimeInput = e => {
		this.setState({integration_time: e.target.value});
	};
	handleXAxisResulotion = e =>{
		this.setState({x_axis_resulotion: e.target.value});
	};
	handleYAxisResulotion = e =>{
		this.setState({y_axis_resulotion: e.target.value});
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
	handleLoadConfigFile = e =>{
		// Check if the file is .json type
		import loadedConfigData from loadedConfigFile;
		
		integration_time:loadedConfigData.text_box.integration_time_micro_sec,//configData.integration_time_micro_sec,
		x_axis_resulotion: loadedConfigData.text_box.x_axis_resulotion,
		y_axis_resulotion:loadedConfigData.text_box.y_axis_resulotion,
		delay_between_pixels_milisec: loadedConfigData.text_box.delay_between_pixels_milisec,
		results_directory: loadedConfigData.text_box.results_directory,
		config_file_name: ""
		  }
		const loadedConfigDataObject={
			text_box:{
				results_directory: this.state.results_directory,
				integration_time_micro_sec: this.state.integration_time,
				x_axis_resulotion: this.state.x_axis_resulotion,
				y_axis_resulotion: this.state.y_axis_resulotion,
				delay_between_pixels_milisec: this.state.delay_between_pixels_milisec
			}
		}
	}

	handleSaveConfigFile = e =>{
		const newConfigDataObject= {
			text_box: {
				results_directory: this.state.results_directory,
				integration_time_micro_sec: this.state.integration_time,
				x_axis_resulotion: this.state.x_axis_resulotion,
				y_axis_resulotion: this.state.y_axis_resulotion,
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

  function loadFile() {
    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
      alert("The file API isn't supported on this browser yet.");
      return;
    }

    input = document.getElementById('fileinput');
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
    }
  }

	
	
	
  //WORK UNTIL HERE
  render(){
  //const [integration_time, setIntegrationTime] = useState('');
  return (
    <div className="App">
    <body>
<form action="" method="post">
<table style={{width: "100%"}}>
	<tr>
		<td className="auto-style1" colspan="3">Welcome</td>
	</tr>
	<tr>
		<td style={{width: "282px"}}>

			<input checked="checked" name="Radio1" type="radio" />Hyper Spectral
			Scan<br />
			<input name="Radio1" type="radio" />WR - White Target Scan
		</td>
		<td className="auto-style1">Choose Configuration
			<input name="loadedConfigFile" id = 'fileInput' type="file"/>
			//onClick={this.handleLoadConfigFile}
			<input 
			type= 'button'
			id = 'buttonLoad'
			value= 'Load'
			onclick='loadFile();'/>
		</td>
		<td className="auto-style1">Date (Calendar) #2F</td>
	</tr>
	<tr>
		<td style={{width: "282px"}}>
		Enter Integration time [micro-Sec]<br />
		<input 
			name ="integration_time_micro_sec"
			type="text"
			onChange={this.handleIntegrationTimeInput}	
			value={this.state.integration_time}/><br />
		Choose X axis resulotion
		<input
			name="x_axis_resulotion"
			type="text"
			onChange={this.handleXAxisResulotion}	
			value={this.state.x_axis_resulotion}/><br />
		</td>
		<td className="auto-style1"><strong>Add units to scan</strong><table style={{width: "100%"}}>
			<tr>
				<td>Unit</td>
				<td>Status</td>
				<td>Add</td>
			</tr>
			<tr>
				<td>All-sky camera</td>
				<td>&nbsp;</td>
				<td>
					<input name="Checkbox1" type="checkbox" value="yes"  />
				</td>
			</tr>
			<tr>
				<td>Radiation sensor</td>
				<td>&nbsp;</td>
				<td><input name="Checkbox2" type="checkbox" /></td>
			</tr>
			<tr>
				<td style={{height: "28px"}}>Thermapp TH</td>
				<td style={{height: "28px"}}></td>
				<td style={{height: "28px"}}>
				<input name="Checkbox3" type="checkbox" /></td>
			</tr>
			<tr>
				<td>GPS</td>
				<td>&nbsp;</td>
				<td><input name="Checkbox4" type="checkbox" /></td>
			</tr>
		</table>
		</td>
		<td className="auto-style1">Timer #2F<br />
		</td>
	</tr>
	<tr>
		<td style={{width: "282px"} , {height: "119px"}}>Choose Y axis resulotion
			<input 
				name="y_axis_resulotion"
				type="text"
				onChange={this.handleYAxisResulotion}	
				value={this.state.y_axis_resulotion}/><br />
		</td>
		<td rowspan="2">

			<div className="auto-style1">
				<br />
				<input 
				name="Submit1" style={{width: "160px"} , {height: "99px"}} type="submit" value="submit" /><br />
			</div>

		<div className="auto-style1">
			&nbsp;Check dummy device state (Ready/Not)</div>
			<div className="auto-style1">
				<input name="Submit2" type="submit" value="Update" /></div>
		</td>
		<td style={{height: "119px"}}>Save&nbsp; the scan in this directory:<br />
		<input 
			name="results_directory"
			style={{width: "400px"}}
			type="text"
			onChange={this.handleResultsDirectory}	
			value={this.state.results_directory}/>
		</td>
	</tr>
	<tr>
		<td style={{width: "282px"}}>Delay between pixels [micro-Sec] <br />
		<input 
			name="delay_between_pixels_milisec" 
			type="text"
			onChange={this.handleDelayBetweenPixels}	
			value={this.state.delay_between_pixels_milisec}/></td>
		<td>Configuration file name
			<input
			name ="config_file_name"
			type="text"
			onChange={this.handleConfigName}	
			value={this.state.config_file_name}
			/>
			<br />
		Save Configuration
			<input 
			name="save_config_button"
			type="button" 
			value="button"
			onClick={this.handleSaveConfigFile}
			/>
		</td>
	</tr>
</table>
 
			
<p>{this.state.integration_time}</p>
<p>{this.state.x_axis_resulotion}</p>
<p>{this.state.y_axis_resulotion}</p>
<p>{this.state.config_file_name}</p>
</form>
</body>




    </div>
  );
  }
}

export default App;
