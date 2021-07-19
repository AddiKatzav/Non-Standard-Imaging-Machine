import React, { Component } from 'react';
import './style.css';
const fs = require("fs");
const yaml = require("js-yaml");

var all_inputs_dict= {
	"text_box" :{
	"results_directory" : "C:\Users\Dell\Desktop\Final_Project\Flask_React_Merged\ScanResults",
    "integration_time_micro_sec" : 300000,
    "x_axis_resulotion" : 40,
    "y_axis_resulotion" : 30,
    "delay_between_pixels_milisec" : 0
	}
}

try {
  const config_data = yaml.load(fs.readFileSync('yaml_data_example.yml', 'utf8'));
  console.log(config_data);
} catch (e) {
  console.log(e);
}



class App extends Component {
  render(){
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
		<td className="auto-style1">Load a configuration
			<input name="File1" type="file" />
		</td>
		<td className="auto-style1">Date (Calendar) #2F</td>
	</tr>
	<tr>
		<td style={{width: "282px"}}>Enter Integration time [micro-Sec]<br />
		<input name="integration_time_micro_sec" type="text" /><br />&nbsp;Choose X axis resulotion<input name="x_axis_resulotion" type="text" />
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

					<input name="Checkbox1" type="checkbox" value= config_data.checkbox.Checkbox1  />
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
			<input name="y_axis_resulotion" type="text" />
		</td>
		<td rowspan="2">

			<div className="auto-style1">
				<br />
				<input name="Submit1" style={{width: "160px"} , {height: "99px"}} type="submit" value="submit" /><br />
			</div>

		<div className="auto-style1">
			&nbsp;Check dummy device state (Ready/Not)</div>
			<div className="auto-style1">
				<input name="Submit2" type="submit" value="Update" /></div>
		</td>
		<td style={{height: "119px"}}>Save&nbsp; the scan in this directory:<br />
		<input name="results_directory" style={{width: "400px"}} type="text" />
		</td>
	</tr>
	<tr>
		<td style={{width: "282px"}}>Delay between pixels [micro-Sec] <br />
		<input name="delay_between_pixels_milisec" type="text" /></td>
		<td>GPS #2F
			<input name="Text4" type="text" /><br />

		Save Configuration
			<input name="Button2" type="button" value="button" />
		</td>
	</tr>
</table>
</form>
</body>




    </div>
  );
  }
}

export default App;
