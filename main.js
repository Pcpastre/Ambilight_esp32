const express = require('express');
const path = require('path');
let fs = require('fs');
const app = express();
const port = process.env.PORT || 4002;
const request = require('request');

var handle = require('./handleFunction.js');
// sendFile will go here

var mac_address = ["98-DE-D0-0E-F3-82", "6C-2B-59-FF-0F-78", "6C-2B-59-FF-0B-FB", "6C-2B-59-FF-09-89", "54-B2-03-1C-5A-C3", "D4-3B-04-0D-28-5C"];

// sendFile will go here
app.get('/', function (req, res) {

	res.sendFile(path.join(__dirname, 'data/index.html'));
});

var key = "=&";
var clientIp = "";
app.get('/key', function (req, res) {
	var para1 = req.query.login;
	var para2 = req.query.senha;
	var keyChar = -1;
	console.log(para1 + para2);
	if (para2 == "roboto2537" && para1 == "admin") {
		clientIp = req.socket.remoteAddress;
		console.log(clientIp);
		key = "";
		for (var i = 0; i < 20; i++) {
			var rando = getRandomInt(0, 3);
			if (rando == 0) {
				keyChar = getRandomInt(48, 57);
			} else if (rando == 1) {
				keyChar = getRandomInt(65, 90);
			} else if (rando == 2) {
				keyChar = getRandomInt(97, 122);
			}
			key = key + String.fromCharCode(keyChar);
		}
		console.log(key);
	} else {
		key = "-1";
	}
	res.send(key);
});

app.get('/conexao', function (req, res) {
	var para1 = req.query.login;
	var para2 = req.query.key;
	console.log(para1 + para2);
	if (para2 == key && para1 == "true" && clientIp == req.socket.remoteAddress) {
		res.sendFile(path.join(__dirname, 'data/controllerPage.html'));
	} else {
		res.status(401).sendFile(path.join(__dirname, 'data/errorPage.html'));
	}

});

app.get('/anima', function (req, res) {
	var para1 = req.query.key;
	console.log(para1);
	if (para1 == key && clientIp == req.socket.remoteAddress) {

		res.sendFile(path.join(__dirname, 'data/animation_robot.html'));
	} else {
		res.status(401).sendFile(path.join(__dirname, 'data/errorPage.html'));
	}

});

function getRandomInt(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min)) + min;
}



app.get('/pcs', function (req, res) {
	var disp = req.query.disp;
	var action = req.query.action;
	console.log(disp + " " + action);
	var device = " ";
	if (disp == "note") {
		device = mac_address[0];
		ipDev = ipsTV[0];
	} else if (disp == "TA") {
		device = mac_address[1];
		ipDev = ipsTV[1];
	} else if (disp == "TB") {
		device = mac_address[2];
		ipDev = ipsTV[2];
	} else if (disp == "TC") {
		device = mac_address[3];
		ipDev = ipsTV[3];
	} else if (disp == "PODIUM") {
		device = mac_address[4];
		ipDev = ipsTV[4];
	}
	if (action == "on") {
		handle.sendWow(device);
	}else{
		request(('http://' + ipDev+ ':4002/turnTV?state=off'), (err, res, body) => {
			if (err) {
				console.log(err);
			} 
		});
	}

});

app.get('/RPI', function (req, res) {
	var disp = req.query.disp;
	var action = req.query.action;
	console.log(disp + " " + action);
	var device;
    if(disp == "R_C"){
      device = 0;
    }else if(disp == "R_B"){
      device = 1;
    }else if(disp == "R_A"){
      device = 2;
    }
    rele(device,action);
  }

	res.sendFile(path.join(__dirname, 'data/index.html'));
});

var serverState = ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"];

app.get('/refresh', function (req, res) {
	var v = req.query.v;
	var vToint = parseInt(v);
	res.send(serverState[vToint]);
});



var localHostVar = ["EntryPoints", "VoiceServer", "Processing", "LightServer", "LearningServer", "ravel-hub-multi"];
var localHost = ["/", ":5555/aaa", ":8000/aaa", ":1111/", ":9090/aaa", ":4000/aaa"];
var botSHost = [":7777/aaa", ":7779/aaa", ":7778/aaa"];
var ipsRPI = ["169.254.1.51", "169.254.1.41", "169.254.1.31"];
var podiumHost = [":1000/aaa", ":6060/aaa ", ":10000/aaa"];
var ipsTV = ["169.254.1.1", "169.254.1.10", "169.254.1.20", "169.254.1.30", "169.254.1.50"];
var count = 0;
setInterval(function () {
	count = 0;
	for (var i = 0; i < 6; i++) {

		request(('http://169.254.1.1' + localHost[i]), (err, res, body) => {
			if (err) {
				serverState[count] = "offline";
			} else {
				serverState[count] = "online";
			}
			count = count + 1;
			//console.log(body.explanation);
		});
	}
	for (var i = 0; i < 3; i++) {
		for (var j = 0; j < 3; j++) {
			request(('http://' + ipsRPI[i] + botSHost[j]), (err, res, body) => {
				if (err) {
					serverState[count] = "offline";
				} else {
					serverState[count] = "online";
				}
				count = count + 1;
				//console.log(body.explanation);
			});

		}
	}
	/*
	for (var j = 0; j < 3; j++) {
		request(('http://169.254.1.50' + podiumHost[j]), (err, res, body) => {
			if (err) {
				serverState[count] = "offline";
			} else {
				serverState[count] = "online";
			}
			count = count + 1;
			//console.log(body.explanation);
		});

	}
	count = 17;
	for (var j = 1; j < 4; j++) {
		request(('http://' + ipsTV[j] + ':1000/started'), (err, res, body) => {
			if (err) {
				serverState[count] = "offline";
			} else {
				serverState[count] = "online";
			}
			count = count + 1;
			//console.log(body.explanation);
		});

	}*/

}, 15000); //2000mSeconds update rate

app.listen(port);
console.log('Server started at http://localhost:' + port);