from flask import Flask, render_template, Response, json, request
import picamera
from io import BytesIO
import os
from flask import jsonify
from flask_cors import CORS, cross_origin
import cv2

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
    with open('static/data/config.json','w') as outfile:
        data[0]['pid'] = True
        json.dump(data,outfile, indent = 1)
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
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    response = jsonify(data)
    return response

@app.route('/reset', methods=["POST"])
def start():
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        
    with open('static/data/config.json','w') as outfile:
        data[0]['start'] = False
        json.dump(data,outfile, indent = 1)

    return "START"


@app.route('/set_regulator', methods=["POST"])
def set_regulator():
    regulator = request.form.get('pid')
    
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        
    with open('static/data/config.json','w') as outfile:
        if regulator == "true":
            data[0]['pid'] = True
        else:
           data[0]['pid'] = False 
        json.dump(data,outfile, indent = 1)
        
    return regulator

@app.route('/set_config', methods=["POST"])
def set_config():
    light = request.form.get('light')
    temp = request.form.get('temp')
    hum = request.form.get('hum')
    
    with open('static/data/config.json','r') as outfile:
        data = json.load(outfile)
        
    with open('static/data/config.json','w') as outfile:
        data[0]['lux'] = light
        data[0]['temp'] = temp
        data[0]['hum'] = hum
        json.dump(data,outfile, indent = 1)
        
    return "Done"
        
@app.route('/')
def main_page():
    return render_template("main.html")  
    
@app.route('/config')
def config():
    return render_template("config.html")  
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 80, debug = True, threaded = True)