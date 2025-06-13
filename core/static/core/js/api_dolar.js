var https = require('https');
https.get('https://mindicador.cl/api', function(res) {
    res.setEncoding('utf-8');
    var data = '';
 
    res.on('data', function(chunk) {
        data += chunk;
    });
    res.on('end', function() {
        var dailyIndicators = JSON.parse(data); // JSON to JavaScript object
        res.send('El valor actual de la UF es $' + dailyIndicators.uf.valor);
    });
 
}).on('error', function(err) {
    console.log('Error al consumir la API!');
});