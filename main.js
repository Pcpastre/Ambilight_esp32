const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 80;

const request = require('request');

var serialHub = require('./serialHub');


var dispositvo = new serialHub("COM4", "teste");

console.log(dispositvo);

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

app.get('/disp', function (req, res) {
	var para1 = req.query.key;

	console.log(para1);
	if (para1 == key && clientIp == req.socket.remoteAddress) {

		res.sendFile(path.join(__dirname, 'data/ledPage.html'));
	} else {
		res.status(401).sendFile(path.join(__dirname, 'data/errorPage.html'));
	}
});

var serverState = ["led1","led2","led3","led4"];
var category = ["led","led","led","led"];

app.get('/getDisp', function (req, res) {
	var v = req.query.v;
	var vToint = parseInt(v);
	console.log(vToint);
	console.log(serverState[vToint]);
	res.send(serverState[vToint]);
});

app.listen(port);
console.log('Server started at http://localhost:' + port);