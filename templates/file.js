var obj = {
    table: []
} ;

obj.table.push({id: 1, square:2});

var json = JSON.stringify(obj);

var fs = require('fs');
fs.writeFile('f.json', json, 'utf8', callback);