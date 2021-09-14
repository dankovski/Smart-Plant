from flask import Flask, render_template, Response, json, request
import picamera
from io import BytesIO
import os
from flask import jsonify
from flask_cors import CORS, cross_origin
import cv2
import time

app = Flask(__name__)
CORS(app)

url = "192.168.0.9"

def gen():
    cam = cv2.VideoCapture(0)
    cam.release()
    cam = cv2.VideoCapture(0)
    
    while True:
        my_stream = BytesIO()
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        if my_stream is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            print("frame is none")
    

@app.route("/charts")
def main():
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        outfile.close()
        data[0]['pid'] = True
    with open('static/data/config.json','w') as outfile:
        json.dump(data,outfile, indent = 1)
        outfile.close()
    return render_template("charts.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")


@app.route("/img")
def image():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_data', methods=["GET"])
@cross_origin()
def get_data():
    filename = os.path.join(app.static_folder, 'data', 'actual_data.json')
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
            response = jsonify(data)
            return response
    except:
        return "error"
   
@app.route('/get_historical_data', methods=["GET"])
@cross_origin()
def get_historical_data():
    filename = os.path.join(app.static_folder, 'data', 'historical_data.json')
    #filename = os.path.join(app.static_folder, 'data', 'test.json')
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
            response = jsonify(data)
            return response
    except:
        return "error"

@app.route('/get_compare_data', methods=["GET"])
@cross_origin()
def get_compare_data():
    filename = os.path.join(app.static_folder, 'data', 'actual_data_pid.json')
    response=[]
    try:
        with open(filename, 'r') as json_file:
            data_pid = json.load(json_file)
            json_file.close()
            response.append(data_pid)
    except:
        return "error"
    filename = os.path.join(app.static_folder, 'data', 'actual_data_fuzzy.json')
    try:
        with open(filename, 'r') as json_file:
            data_fuzzy = json.load(json_file)
            json_file.close()
            response.append(data_fuzzy)
    except:
        return "error"
    return jsonify(response)


@app.route('/reset', methods=["POST"])
def start():
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        outfile.close()
        data[0]['start'] = False
    with open('static/data/config.json','w') as outfile:
        json.dump(data,outfile, indent = 1)
        outfile.close()
    return "START"


@app.route('/set_regulator', methods=["POST"])
def set_regulator():
    regulator = request.form.get('pid')
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        outfile.close()
        if regulator == "true":
            data[0]['pid'] = True
        else:
           data[0]['pid'] = False 
    with open('static/data/config.json','w') as outfile:
        json.dump(data,outfile, indent = 1)
        outfile.close()
    return regulator

@app.route('/set_config', methods=["POST"])
def set_config():
    light = request.form.get('light')
    temp = request.form.get('temp')
    hum = request.form.get('hum')
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        outfile.close()
        data[0]['lux'] = light
        data[0]['temp'] = temp
        data[0]['hum'] = hum
    with open('static/data/config.json','w') as outfile:
        json.dump(data,outfile, indent = 1)
        outfile.close()
    return "Done"

@app.route('/get_config', methods=["GET"])
def get_config():
    try:
        with open('static/data/config.json','r') as outfile:
            data = json.load(outfile)
            outfile.close()
            return jsonify(data)
    except:
        return "Failed"
   
@app.route('/')
def main_page():
    return render_template("main.html")  
    
@app.route('/config')
def config():
    return render_template("config.html")  
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 80, debug = True, threaded = True)