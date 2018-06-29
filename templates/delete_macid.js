var macId = undefined;
chrome.storage.local.get( null, function(item){

    chrome.storage.local.remove('machine-id')

    console.log(item['machine-id']);


    chrome.storage.local.remove('database')

    chrome.storage.local.remove('lastUpdate')

    console.log(item['database']);
   chrome.storage.local.remove('res')

   console.log(item['res']);

});

//delete_macid.js
//machine-id