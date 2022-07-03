const express = require('express');
const path = require('path');
var http = require('http');
const app = express();
const port = process.env.PORT || 80;

const request = require('request');

app.get('/', function (req, res) {

	res.sendFile(path.join(__dirname, 'data/index.html'));
});

app.get('/mode', function (req, res) {

	M = req.query.M;
	url = "http://192.168.0.102/mode?M=" + M;

	http.get(url, (resp) => {
		
		// A chunk of data has been recieved.
		resp.on('data', (chunk) => { });
		resp.on('end', () => { });

	}).on("error", (err) => {
		console.log(err);
	});
	res.send("okay");
});

app.get('/color', function (req, res) {

	r = req.query.r;
	g = req.query.g;
	b = req.query.b;
	url = "http://192.168.0.102/colorSend?R=" + r+"&G="+g+"&B="+b;
	console.log(url);
	http.get(url, (resp) => {
		
		// A chunk of data has been recieved.
		resp.on('data', (chunk) => { });
		resp.on('end', () => { });

	}).on("error", (err) => {
		console.log(err);
	});
	res.send("okay");
});


app.get('/SonOff', function (req, res) {

	serv = req.query.service;
	mode = req.query.mode;
	if(serv == "wave"){
		if(mode == "on"){
			url = "http://localhost:1000/Start";
		}else if(mode == "off"){
			url = "http://localhost:1000/Stop";
		}
	}else if("color"){
		if(mode == "on"){
			url = "http://localhost:1001/Start";
		}else if(mode == "off"){
			url = "http://localhost:1001/Stop";
		}
	}

	http.get(url, (resp) => {
		
		// A chunk of data has been recieved.
		resp.on('data', (chunk) => { });
		resp.on('end', () => { });

	}).on("error", (err) => {
		console.log(err);
	});
	res.send("okay");
});

var key = "=&";
var clientIp = "";
app.get('/key', function (req, res) {
	var para1 = req.query.login;
	var para2 = req.query.senha;
	var keyChar = -1;
	console.log(para1 + para2);
	if (para2 == "123456" && para1 == "admin") {
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

function getRandomInt(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min)) + min;
}

app.get('/conexao', function (req, res) {
	var para1 = req.query.login;
	var para2 = req.query.key;
	if(para2 == key){
		res.sendFile(path.join(__dirname, 'data/controllerPage.html'));
	}
});

app.listen(port);
console.log('Server started at http://localhost:' + port);