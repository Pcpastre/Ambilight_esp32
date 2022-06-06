const wol = require('wol');

var self = module.exports = {
	
	sendWow: function (disp) {
		wol.wake(disp, function(err, res){
			console.log(res);
		});
        
    }
	
}