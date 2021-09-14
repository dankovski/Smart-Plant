class Config{ 
	constructor(hum,temp,light){
		this.hum = hum;
		this.temp= temp;
		this.light = light;
	}
}

var radish = new Config(70, 18, 1000);
var bean = new Config(70, 22, 1200);
var paprica = new Config(50, 20, 1200);
var marigold = new Config(20, 21, 800);

$( document ).ready(function() {
	updateActualValues();
  });

function presetHandler(name){
    document.getElementById('hum').value = name.hum;
    document.getElementById('temp').value = name.temp;
    document.getElementById('light').value = name.light;
}

function updateActualValues(){
	$.ajax({
        url: "/get_config",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {

			document.getElementById('hum').placeholder = "actual: " + parseFloat(responseJSON[0]['hum']) + " %";
			document.getElementById('temp').placeholder = "actual: " + parseFloat(responseJSON[0]['temp']) + " °C";
			document.getElementById('light').placeholder = "actual: " + parseFloat(responseJSON[0]['lux']) + " lx";

    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});
}


function saveHandler(){
	
	let temp_hum = parseFloat(document.getElementById('hum').value);
	let temp_temp = parseFloat(document.getElementById('temp').value);
	let temp_light = parseFloat(document.getElementById('light').value);
    

	document.getElementById('hum').value= " ";
	document.getElementById('temp').value = " ";
	document.getElementById('light').value = "";

	document.getElementById('hum').placeholder = "actual: " + temp_hum + " %";
	document.getElementById('temp').placeholder = "actual: " + temp_temp + " °C";
	document.getElementById('light').placeholder = "actual: " + temp_light + " lx";

    $.ajax({
		url: "/set_config",
		data: {'light': temp_light, 'temp': temp_temp, 'hum': temp_hum},
		type: 'POST',
		dataType: 'text/json',
		success: function(response){
			console.log(response);
		},
		failure: function(response){
			console.log(response);}
		});


}