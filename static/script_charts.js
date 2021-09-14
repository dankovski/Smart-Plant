

var charts=new Array(0);
var chartsContext=new Array(0);

var ydata_temp=new Array(0);
var ydata_light=new Array(0);
var ydata_hum=new Array(0);
var ydata_pwm=new Array(0);

var ydata_temp_desired=new Array(0);
var ydata_light_desired=new Array(0);
var ydata_hum_desired=new Array(0);

var desired_lux;
var desired_hum;
var desired_temp;

var ydata_compare_pid = new Array(0);
var ydata_compare_fuzzy = new Array(0);


var xdata=new Array(0);
var timer;

var start = false
var pid = true
var historical = true

function init(){
load_config();
chartsInit();



var slider = document.getElementById('slider');

noUiSlider.create(slider, {
    start: [0, 100],
    step:1,
    connect: true,
    range: {
        'min': 0,
        'max': 100
    }
});


set_historical();

}

function set_actual(){
    var historical_elements = document.getElementsByClassName('historical');
    for (var i=0; i<historical_elements.length; i++){
    historical_elements[i].style.display = "none";
    }

    var actual_elements = document.getElementsByClassName('actual');
    for (var i=0; i<actual_elements.length; i++){
    actual_elements[i].style.display = "block";
    }


    historical = false;

    var button_3days = document.getElementById("button_3days");
    button_3days.style.backgroundColor = "blue";


    var button_30s = document.getElementById("button_30s");
    button_30s.style.backgroundColor = "green";


}

function set_historical(){
    var actual_elements = document.getElementsByClassName('actual');
    for (var i=0; i<actual_elements.length; i++){
    actual_elements[i].style.display = "none";
    }
    var historical_elements = document.getElementsByClassName('historical');
    for (var i=0; i<historical_elements.length; i++){
    historical_elements[i].style.display = "block";
    }

    historical = true;

    var button_3days = document.getElementById("button_3days");
    button_3days.style.backgroundColor = "green";


    var button_30s = document.getElementById("button_30s");
    button_30s.style.backgroundColor = "blue";

}


function newChart(xData,yData,xlabel,ylabel, context){
        chart = new Chart(context, {
    
            type: 'line',
    
            data: {
                labels: xData,
                datasets: [
                {
                    borderWidth:2,
                    fill: false,
                    label: "actual",
                    backgroundColor: 'rgb(255, 0, 0)',
                    borderColor: 'rgb(255, 0, 0)',
                    data: yData,
                    lineTension: 0.1
                },
                {
                    borderWidth:2,
                    fill: false,
                    label: "desired",
                    backgroundColor: 'rgb(0, 0, 255)',
                    borderColor: 'rgb(0, 0, 255)',
                    data: yData,
                    lineTension: 0.1
                }
            
            ]
            },
            // Configuration options
            options: {
                elements:{
                    point:{
                        radius:0
                    }
                },
                legend: {
                    display: true
                },
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: ylabel
                        }
                    }],
                    xAxes: [
                        {ticks: {
                        precision:0,
						stepSize: 1
						},
                        scaleLabel: {
                            display: true,
                            labelString: xlabel
                        }
                    }]
                }
            }
        });
    
        return chart
    }


function newHistoricalChart(xData,yData,xlabel,ylabel, context){
        chart = new Chart(context, {
    
            type: 'line',
    
            data: {
                labels: xData,
                datasets: [
                {
                    borderWidth:2,
                    fill: false,
                    label: "historical",
                    backgroundColor: 'rgb(255, 0, 0)',
                    borderColor: 'rgb(255, 0, 0)',
                    data: yData,
                    lineTension: 0.1
                }            
            ]
            },
            // Configuration options
            options: {
                elements:{
                    point:{
                        radius:0
                    }
                },
                legend: {
                    display: true
                },
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: ylabel
                        }
                    }],
                    xAxes: [
                        {
                        ticks: {
                        precision:0,
						stepSize: 1
						},
                        scaleLabel: {
                            display: true,
                            labelString: xlabel
                        }
                    }]
                }
            }
        });
    
        return chart
    }

function loadData() {

if(historical){
    $.ajax({
        url: "/get_historical_data",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {


            ydata_temp = new Array(0)
            ydata_light = new Array(0)
            ydata_hum = new Array(0)
            xdata = new Array(0)

    
            for(let i=0; i<responseJSON.length; i++){
                ydata_temp.push(parseFloat(responseJSON[i]['Temperature']))
                ydata_light.push(parseFloat(responseJSON[i]['Light']))
                ydata_hum.push(parseFloat(responseJSON[i]['Humidity']))
                //xdata.push(parseFloat(responseJSON[i]['date']))
                xdata.push(responseJSON[i]['date'])
            }
    
            charts[5].data.datasets[0].data = ydata_light
            charts[5].data.labels = xdata
            charts[5].update();
            charts[6].data.datasets[0].data = ydata_temp
            charts[6].data.labels = xdata
            charts[6].update();
            charts[7].data.datasets[0].data = ydata_hum
            charts[7].data.labels = xdata
            charts[7].update();








    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});
}
else{
	$.ajax({
        url: "/get_data",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {

        ydata_temp = new Array(0)
        ydata_light = new Array(0)
        ydata_hum = new Array(0)
        xdata = new Array(0)
        ydata_pwm = new Array(0)

        for(let i=0; i<responseJSON.length; i++){
            ydata_temp.push(parseFloat(responseJSON[i]['Temperature']))
            ydata_light.push(parseFloat(responseJSON[i]['Light']))
            ydata_hum.push(parseFloat(responseJSON[i]['Humidity']))
            ydata_pwm.push(parseFloat(responseJSON[i]['pwm']))
            ydata_light_desired.push(desired_lux)
            ydata_hum_desired.push(desired_hum)
            ydata_temp_desired.push(desired_temp)
            xdata.push(parseFloat(responseJSON[i]['t']))  
        }

        charts[0].data.datasets[0].data = ydata_light
        charts[0].data.datasets[1].data = ydata_light_desired
        charts[0].data.labels = xdata
        charts[0].update();
        charts[1].data.datasets[0].data = ydata_temp
        charts[1].data.labels = xdata
        charts[1].data.datasets[1].data = ydata_temp_desired
        charts[1].update();
        charts[2].data.datasets[0].data = ydata_hum
        charts[2].data.labels = xdata
        charts[2].data.datasets[1].data = ydata_hum_desired
        charts[2].update();
        charts[3].data.datasets[0].data = ydata_pwm
        charts[3].data.labels = xdata
        charts[3].update();
    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});

    $.ajax({
        url: "/get_compare_data",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {

            ydata_compare_pid = new Array(0)
            ydata_compare_fuzzy = new Array(0)
            xdata = new Array(0)
            
            if (responseJSON[0].length >= responseJSON[1].length){
                length = responseJSON[0].length;
            }
            else{
                length = responseJSON[1].length;
            }
            
            var slider = document.getElementById('slider');

            for(let i=0; i<length; i++){
                if (i<responseJSON[0].length){
                    ydata_compare_pid.push(parseFloat(responseJSON[0][i]['Light']));
                    xdata.push(parseFloat(responseJSON[0][i]['t']));
                }
                else{
                    xdata.push(parseFloat(responseJSON[1][i]['t']));
                }

                if(i<responseJSON[1].length){
                    ydata_compare_fuzzy.push(parseFloat(responseJSON[1][i]['Light']));
                    
                }
                
                
            }
    
    ydata_compare_pid = ydata_compare_pid.slice(length*slider.noUiSlider.get()[0]/100.0, length*slider.noUiSlider.get()[1]/100.0);
    ydata_compare_fuzzy = ydata_compare_fuzzy.slice(length*slider.noUiSlider.get()[0]/100.0, length*slider.noUiSlider.get()[1]/100.0);
    xdata = xdata.slice(length*slider.noUiSlider.get()[0]/100.0, length*slider.noUiSlider.get()[1]/100.0);



            charts[4].data.datasets[0].data = ydata_compare_pid
            charts[4].data.datasets[1].data = ydata_compare_fuzzy
            charts[4].data.labels = xdata
            charts[4].update();



    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});
}


}

function chartsInit(){
    chartsContext.push(document.getElementById("chart_light").getContext('2d'))
    chartsContext.push(document.getElementById("chart_temp").getContext('2d'));
    chartsContext.push(document.getElementById("chart_hum").getContext('2d'));
    chartsContext.push(document.getElementById("chart_pwm").getContext('2d'));
    chartsContext.push(document.getElementById("chart_compare").getContext('2d'));
    chartsContext.push(document.getElementById("chart_light_historical").getContext('2d'))
    chartsContext.push(document.getElementById("chart_temp_historical").getContext('2d'));
    chartsContext.push(document.getElementById("chart_hum_historical").getContext('2d'));

    charts.push(newChart(xdata, ydata_light, "Time[s]", "Light intensity[lx]", chartsContext[0]))
    charts.push(newChart(xdata, ydata_temp, "Time[s]", "Temperature[°C]", chartsContext[1]))
    charts.push(newChart(xdata, ydata_hum, "Time[s]", "Humidity[%]", chartsContext[2]))
    charts.push(newChart(xdata, ydata_pwm, "Time[s]", "PWM[%]", chartsContext[3]))
    charts[3].data.datasets.splice(1,1);
    charts[3].update();

    charts.push(newChart(xdata, ydata_compare_pid, "Time[s]", "Light intensity[lx]", chartsContext[4]))
    charts[4].data.datasets[0].label = "PID";
    charts[4].data.datasets[1].label = "FUZZY";
    charts[4].update();

    charts.push(newHistoricalChart(xdata, ydata_light, "Time[s]", "Light intensity[lx]", chartsContext[5]))


    charts.push(newChart(xdata, ydata_temp, "Time[s]", "Temperature[°C]", chartsContext[6]))
    charts[6].data.datasets.splice(1,1);
    charts[6].data.datasets[0].label = "historical";
    charts[6].update();

    charts.push(newChart(xdata, ydata_hum, "Time[s]", "Humidity[%]", chartsContext[7]))
    charts[7].data.datasets.splice(1,1);
    charts[7].data.datasets[0].label = "historical";
    charts[7].update();

}

function start_work(){

    if (start == false){

        var button_start = document.getElementById("start");
        button_start.style.backgroundColor = "green";
        button_start.style.borderColor = "black";
    
        var button_stop = document.getElementById("stop");
        button_stop.style.backgroundColor = "blue";
        button_stop.style.borderColor = "transparent";
    

        start = true

    if(!historical){

    $.ajax({
        url: "/reset",
		type: 'POST', 
        dataType: 'text',
        data: 'asd',
		success: function(response, status, xhr) {
            console.log(response); 

    },
    error: function (ajaxContext) {
            console.log("Error while getting data from server");
    }
	});
    }


	timer = setInterval(loadData, 2000);


    }

}

function stop_work(){
    if(start){
        clearInterval(timer);
        start = false;
        var button_stop = document.getElementById("stop");
        button_stop.style.backgroundColor = "green";
        button_stop.style.borderColor = "black";
    
        var button_start = document.getElementById("start");
        button_start.style.backgroundColor = "blue";
        button_start.style.borderColor = "transparent";
    }

}

function start_pid(){

    if (pid == false){

        if(start){
            clearInterval(timer);
            start = false;
            var button_stop = document.getElementById("stop");
            button_stop.style.backgroundColor = "green";
            button_stop.style.borderColor = "black";
        
            var button_start = document.getElementById("start");
            button_start.style.backgroundColor = "blue";
            button_start.style.borderColor = "transparent";
        }

        pid = true;
        var button_pid = document.getElementById("pid");
        button_pid.style.backgroundColor = "green";
        button_pid.style.borderColor = "black";
    
        var button_fuzzy = document.getElementById("fuzzy");
        button_fuzzy.style.backgroundColor = "blue";
        button_fuzzy.style.borderColor = "transparent";
    

    $.ajax({
        url: "/set_regulator",
		type: 'POST', 
        dataType: 'text',
        data: {'pid': true},
		success: function(response, status, xhr) {
            console.log(response); 

    },
    error: function (ajaxContext) {
            console.log("Error while getting data from server");
    }
	});

    }

}

function start_fuzzy(){

    if (pid == true){

        if(start){
            clearInterval(timer);
            start = false;
            var button_stop = document.getElementById("stop");
            button_stop.style.backgroundColor = "green";
            button_stop.style.borderColor = "black";
        
            var button_start = document.getElementById("start");
            button_start.style.backgroundColor = "blue";
            button_start.style.borderColor = "transparent";
        }

        pid = false;

        var button_fuzzy = document.getElementById("fuzzy");
        var button_pid = document.getElementById("pid");

        button_fuzzy.style.backgroundColor = "green";
        button_fuzzy.style.borderColor = "black";
    
        
        button_pid.style.backgroundColor = "blue";
        button_pid.style.borderColor = "transparent";
    


    $.ajax({
        url: "/set_regulator",
		type: 'POST', 
        dataType: 'text',
        data: {'pid': false},
		success: function(response, status, xhr) {
            console.log(response); 

    },
    error: function (ajaxContext) {
            console.log("Error while getting data from server");
    }
	});

    }

}


function load_config(){

    $.ajax({
        url: "/get_config",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {



            desired_hum=parseFloat(responseJSON[0]['hum'])
            desired_lux=parseFloat(responseJSON[0]['lux'])
            desired_temp=parseFloat(responseJSON[0]['temp'])
            var sample_time = document.getElementById("sampletime");
            sample_time.innerText = parseFloat(responseJSON[0]['dt'])
            var kp = document.getElementById("kp");
            kp.innerText = parseFloat(responseJSON[0]['kp'])
            var ki = document.getElementById("ki");
            ki.innerText = parseFloat(responseJSON[0]['ki'])
            var kd = document.getElementById("kd");
            kd.innerText = parseFloat(responseJSON[0]['kd'])


    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});

}