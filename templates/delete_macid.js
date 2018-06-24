var macId = undefined;
chrome.storage.local.get( null, function(item){

    chrome.storage.local.remove('machine-id')

    console.log(item['machine-id']);


    chrome.storage.local.remove('database')

    console.log(item['database']);

});

//delete_macid.js
//machine-id