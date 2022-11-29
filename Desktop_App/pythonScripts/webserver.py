import time

from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json, math, os, os.path

PATH_FILES = os.path.dirname(os.path.abspath(__file__)) + "/"
app = Flask(__name__)
ip = "http://192.168.0.162/"

@app.route('/')
def init():
    return render_template("controllerPage.html")


@app.route('/mode')
def mode():
    global ip
    M  = request.args.get('M')
    url = ip+ "mode?M=" + M
    req = requests.get(url)
    req.status_code
    return "okay"



def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

@app.route('/color')
def color():
    global ip
    r  = request.args.get('r')
    g  = request.args.get('g')
    b  = request.args.get('b')
    url = ip+ "colorSend?R=" + r+"&G="+g+"&B="+b
    req = requests.get(url)
    req.status_code
    return "okay"

@app.route('/colorEnd')
def colorEnd():
    global ip
    r  = int(request.args.get('r'))
    g  = int(request.args.get('g'))
    b  = int(request.args.get('b'))
    c = rgb_to_hex((r,g,b))
    url = ip + "colorSend2?&C1="+ c + "&C2=" + c + "&C3=" + c + "&C4=" + c 
    req = requests.get(url)
    req.status_code
    return "okay"

@app.route('/SonOff')
def SonOff():
    global ip
    serv = request.args.get('service')
    mode  = request.args.get('mode')
    if(serv == "wave"):
        if(mode == "on"):
            url = "http://localhost:1000/Start"
        elif(mode == "off"):
            url = "http://localhost:1000/Stop"
    elif(serv =="color"):
        if(mode == "on"):
            url = "http://localhost:1001/Start"
        elif(mode == "off"):
            url = "http://localhost:1001/Stop"
    elif(serv =="color2"):
        if(mode == "on"):
            url = "http://localhost:1001/StartM"


    req = requests.get(url)
    req.status_code
    return "okay"

if __name__ == '__main__':

   # Para lidar com o CTRL+C
   app.run(host='0.0.0.0', port=80,debug=True)