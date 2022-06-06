const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 80;

const request = require('request');

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

function getRandomInt(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min)) + min;
}


app.listen(port);
console.log('Server started at http://localhost:' + port);