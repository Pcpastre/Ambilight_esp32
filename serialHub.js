var SerialPort = require("serialport");
const Readline = require('@serialport/parser-readline');

// Read the port data
var port = 3000;

var arduinoCOMPort = "COM3";

var arduinoSerialPort = new SerialPort({ path: arduinoCOMPort , baudRate: 9600 })

module.exports = class serialHub{
    constructor(disp, nameGiv) {
        this.name = nameGiv;
        
        this.port = port;
    }

}
/*var self = module.exports = {
    creat :  function (disp, nameGive){
        var name = nameGive
        var port = new SerialPort(disp, { baudRate: 9600 });
        const parser = port.pipe(new Readline({ delimiter: '\n' }));
        port.on("open", () => {
            console.log('serial port open');
          });
    },

    Serialwrite : function (disp, port, parser) {
       
          parser.on('data', data =>{
            console.log('got word from arduino:', data);
          });
    
    }
}*/
