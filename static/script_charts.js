

var charts=new Array(0);
var chartsContext=new Array(0);

var ydata_temp=new Array(0);
var ydata_light=new Array(0);
var ydata_hum=new Array(0);
var xdata=new Array(0);
var timer;

var start = false
var pid = true

function init(){
chartsInit();
}


function newChart(name,xData,yData,xlabel,ylabel,ymin,ymax,context){
        chart = new Chart(context, {
    
            type: 'line',
    
            data: {
                labels: xData,
                datasets: [{
                    borderWidth:2,
                    fill: false,
                    label: name,
                    backgroundColor: 'rgb(255, 255, 255)',
                    borderColor: 'rgb(0, 0, 255)',
                    data: yData,
                    lineTension: 0.1
                }]
            },
            // Configuration options
            options: {
                elements:{
                    point:{
                        radius:0
                    }
                },
                legend: {
                    display: false
                },
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: ylabel
                        },
                        ticks: {
                            suggestedMin: ymin,
                            suggestedMax: ymax
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

function loadData() {

	$.ajax({
        url: "/get_data",
		type: 'GET', 
        dataType: 'json',
		success: function(responseJSON, status, xhr) {

        ydata_temp=new Array(0)
        ydata_light=new Array(0)
        ydata_hum=new Array(0)
        xdata=new Array(0)

        for(let i=0; i<responseJSON.length; i++){
            ydata_temp.push(parseFloat(responseJSON[i]['Temperature']))
            ydata_light.push(parseFloat(responseJSON[i]['Light']))
            ydata_hum.push(parseFloat(responseJSON[i]['Humidity']))
            xdata.push(parseFloat(responseJSON[i]['t']))
            
        }

        charts[0].data.datasets[0].data = ydata_light
        charts[0].data.labels = xdata
        charts[0].update();
        charts[1].data.datasets[0].data = ydata_temp
        charts[1].data.labels = xdata
        charts[1].update();
        charts[2].data.datasets[0].data = ydata_hum
        charts[2].data.labels = xdata
        charts[2].update();
    },
        error: function (ajaxContext) {
            console.log("Error while getting data from server");
        },

	});
}

function chartsInit(){
    chartsContext.push(document.getElementById("chart_light").getContext('2d'))
    chartsContext.push(document.getElementById("chart_temp").getContext('2d'));
    chartsContext.push(document.getElementById("chart_hum").getContext('2d'));

    charts.push(newChart("asd", xdata, ydata_light, "Time[s]", "Light intensity[lx]", 0.0, 1300.0, chartsContext[0]))
    charts.push(newChart("asd", xdata, ydata_temp, "Time[s]", "Temperature['C]", 10.0, 30.0, chartsContext[1]))
    charts.push(newChart("asd", xdata, ydata_hum, "Time[s]", "Humidity[%]", 0.0, 100.0, chartsContext[2]))
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

	timer = setInterval(loadData, 1000);




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
