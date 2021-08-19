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

function presetHandler(name){
	
    document.getElementById('hum').value = name.hum;
    document.getElementById('temp').value = name.temp;
    document.getElementById('light').value = name.light;
}

function saveHandler(){
	
	let temp_hum = parseFloat(document.getElementById('hum').value);
	let temp_temp = parseFloat(document.getElementById('temp').value);
	let temp_light = parseFloat(document.getElementById('light').value);
    
    $.ajax({
		url: "/set_config",
		data: {'light': temp_light, 'temp': temp_temp, 'hum': temp_hum},
		type: 'POST',
		dataType: 'text/json',
		success: function(response){console.log(response);},
		failure: function(response){console.log(response);}
		});

}