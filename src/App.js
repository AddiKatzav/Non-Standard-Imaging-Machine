import React, { Component } from 'react';
import './style.css';
import configData from './data_config.json';



var FileSaver = require('file-saver');
var input, file, fr;

const fetchData = () => {
return fetch("http://127.0.0.1:5000/")
      .then((response) => response.json())
      .then((data) => console.log(data));}


function loadFile() {
// This function loads a configuration file
  return new Promise((resolve,reject)=> {
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
	// After loading the file, we load and recieve the text that within the configuration file.
    function receivedText(e) {
      let lines = e.target.result;
      var newArr = JSON.parse(lines);
	  console.log(newArr.text_box);
	  var newState ={
		    first_integration_time: newArr.text_box.first_integration_time_micro_sec,
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
    first_integration_time : configData.text_box.first_integration_time_micro_sec,//configData.integration_time_micro_sec,
	second_integration_time : configData.text_box.second_integration_time_micro_sec,
	third_integration_time : configData.text_box.third_integration_time_micro_sec,
	x_axis_resolution : configData.text_box.x_axis_resolution,
	y_axis_resolution : configData.text_box.y_axis_resolution,
	FOV_X : configData.text_box.FOV_X,
	FOV_Y : configData.text_box.FOV_Y,
	delay_between_pixels_milisec : configData.text_box.delay_between_pixels_milisec,
	results_directory : configData.text_box.results_directory,
	resX_Error : "",
	resY_Error : "",
	ratio_Error : "",
	integration_time_Error : "",
	config_file_name : ""
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
		var file_name = this.state.config_file_name;
		var file_name_json = file_name.concat('.json');
		var blob= new Blob([jsonConfigData],{type : 'application/json'});
		FileSaver.saveAs(blob,file_name.concat(".json"));
	};
	
	// validate function- validate the user inputs according to the spectrometer specifications and spatial scanning logic.
	validate = () =>{
		let resX_Error = "";
		let resY_Error = "";
		let ratio_Error = "";
		let integration_time_Error = "";
		let fov_i = 1.2;
		let max_integration_time = 65*1000000; //max value is 65 second according to the VIS spectrometer
		let min_integration_time = 1*1000; // min value is 1 milisecond according to the VIS spectrometer
	
		if ((this.state.FOV_X)*(this.state.y_axis_resolution)!=(this.state.FOV_Y)*(this.state.x_axis_resolution)){
			// Checking whether ratio of FOV not equal to resolutions
			ratio_Error = 'The ratio of FOV is not equal to resolution ratio!';
			alert(ratio_Error);
			return false;
		}
		if (this.state.first_integration_time == 0 && this.state.second_integration_time == 0 && this.state.third_integration_time){
			// Check Non-Zero Value
			integration_time_Error = "Please enter at least one non-zero integration time";
			alert(integration_time_Error);
			return false;
		}
		if ( this.state.first_integration_time < min_integration_time && this.state.first_integration_time > 0){
			// Too short integ time
			integration_time_Error = 'First integration time is too short! Please enter a longer integration time';
			alert(integration_time_Error);
			return false;
		}
		if ( this.state.second_integration_time < min_integration_time && this.state.second_integration_time > 0){
			// Too short integ time
			integration_time_Error = 'Second integration time is too short! Please enter a longer integration time';
			alert(integration_time_Error);
			return false;
		}
		if ( this.state.third_integration_time < min_integration_time && this.state.third_integration_time > 0){
			// Too short integ time
			integration_time_Error = 'Third integration time is too short! Please enter a longer integration time';
			alert(integration_time_Error);
			return false;
		}
		
		if (this.state.first_integration_time > max_integration_time || this.state.second_integration_time > max_integration_time|| this.state.third_integration_time > max_integration_time){
			// Too long integ time
			integration_time_Error = 'Integration time is too long! Please enter a shorter integration time';
			alert(integration_time_Error);
			return false;
		}
		if ((this.state.x_axis_resolution)*fov_i < this.state.FOV_X){
			// Check if resolution is low, need to enter higher res
			resX_Error = 'X axis resolution is too low! Please enter a higher resolution';
			alert(resX_Error);
			return false;
		}
		if ((this.state.y_axis_resolution)*fov_i < this.state.FOV_Y){
			// Check if resolution is high, need to enter higher res
			resY_Error = 'Y axis resolution is too low, Please enter a higher resolution';
			alert(resY_Error);
			return false;
		}
		return true;
	};

	handleSubmit = event =>{
		
	const isValid = this.validate();
	if (isValid){
		let submit_values = "First integration time :" + this.state.first_integration_time + "\n"
		+ "Second integration time :" + this.state.second_integration_time + "\n"
		+ "Third integration time :" + this.state.third_integration_time + "\n"
		+ "X axis resolution :" + this.state.x_axis_resolution + "\n"
		+ "Y axis resolution :" + this.state.y_axis_resolution + "\n"
		+ "FOV X :" + this.state.FOV_X + "\n"
		+ "FOV Y :" + this.state.FOV_Y + "\n"
		+ "Delay between pixels [milisec] :" + this.state.delay_between_pixels_milisec + "\n"
		+ "Results saved in :" + this.state.results_directory + "\n"
		alert(submit_values);
		this.setState(prevState =>({
			x_axis_resolution: prevState.x_axis_resolution,
			y_axis_resolution: prevState.y_axis_resolution,
			first_integration_time: prevState.first_integration_time,
			second_integration_time: prevState.second_integration_time,
			third_integration_time: prevState.third_integration_time,
			FOV_X: prevState.FOV_X,
			FOV_Y: prevState.FOV_Y,
			delay_between_pixels_milisec: prevState.delay_between_pixels_milisec,
			results_directory: prevState.results_directory,
			resX_Error: "",
			resY_Error: "",
			ratio_Error: "",
			integration_time_Error: "",
			config_file_name: ""
		}));
	}else{
		event.preventDefault();
	}
	};
	
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
				
				<button
				name="submit_activate"
				type="submit" value="Activate" 
				style={{ backgroundColor: "Green" , width: "120px" , height: "60px", fontWeight: "bold", fontSize:14}}>Activate</button>	
				<br />
				
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
</form>
</body>
</div>
  );
  }
}

export default App;
