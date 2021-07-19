import React from "react";

const initialState = {
  name: "",
  email: "",
  password: "",
  nameError: "",
  emailError: "",
  passwordError: ""
  
};

export default class ValiationForm extends React.Component {
  state = initialState;

  validate = () => {
    let resX_Error = "";
    let resY_Error = "";
    let FOV_X_Error = "";
	let FOV_Y_Error = "";
	let integ_time_1_Error = "";
	let integ_time_2_Error = "";
	let integ_time_3_Error = "";
	

    if (emailError || nameError) {
      this.setState({ emailError, nameError });
      return false;
    }

    return true;
  };

  handleSubmit = event => {
    event.preventDefault();
    const isValid = this.validate();
    if (isValid) {
      console.log(this.state);
      // clear form
      this.setState(initialState);
    }
  };

  render() {
    return (
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
          <input
            name="name"
            placeholder="name"
            value={this.state.name}
            onChange={this.handleChange}
          />
          <div style={{ fontSize: 12, color: "red" }}>
            {this.state.nameError}
          </div>
        
        <div>
          <input
            name="email"
            placeholder="email"
            value={this.state.email}
            onChange={this.handleChange}
          />
          <div style={{ fontSize: 12, color: "red" }}>
            {this.state.emailError}
          </div>
        </div>
        <div>
          <input
            type="password"
            name="password"
            placeholder="password"
            value={this.state.password}
            onChange={this.handleChange}
          />
          <div style={{ fontSize: 12, color: "red" }}>
            {this.state.passwordError}
          </div>
        </div>
        <button type="submit">submit</button>
      </form>
	 </body>
    );
  }
}	