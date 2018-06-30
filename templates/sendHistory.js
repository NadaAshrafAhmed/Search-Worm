function sendHistory(storedMacId,numOfLinks){

    chrome.history.search({text: '', maxResults: numOfLinks}, function(data){

        var urls=[]

        data.forEach(function(page) {
            console.log(page.url);
            urls.push(String(page.url))
        });

        var xmlhttp = new XMLHttpRequest();


        xmlhttp.open("POST", "http://127.0.0.1:5000/history");
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ID:storedMacId, urls: urls}));
//        var today = new Date();
//        chrome.storage.local.set({'lastUpdate':{'day':today.getDate(),'month':today.getMonth()+1,"year":today.getFullYear()}});

        xmlhttp.onreadystatechange=function(){

            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
               var res = JSON.parse(xmlhttp.responseText);
               console.log(res) ;

               //writing on file
               chrome.storage.local.set({'res':res});
               var today = new Date();
               chrome.storage.local.set({'lastUpdate':{'day':today.getDate(),'month':today.getMonth()+1,"year":today.getFullYear()}});
            }
        }


    });
}