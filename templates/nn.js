chrome.history.search({text: '', maxResults: 10}, function(data) {

    var urls=[]

    data.forEach(function(page) {
        console.log(page.url);
        urls.push(String(page.url))
    });
    var xmlhttp = new XMLHttpRequest();


    xmlhttp.open("POST", "http://127.0.0.1:5000/history");
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify({ urls: urls}));

   // xmlhttp.open("POST",encodeURI("http://127.0.0.1:5000/history"+urls),true);

    //xmlhttp.open("GET",chrome.extension.getURL("http://127.0.0.1:5000/history"),true);
//    xmlhttp.send();
    xmlhttp.onreadystatechange=function()
                {
                    if (xmlhttp.readyState==4 && xmlhttp.status==200)
                    {
                       console.log(xmlhttp.responseText);
                    }
                }

    });
