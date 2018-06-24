

chrome.storage.local.get('machine-id', function(item){

  var storedMacId = item['machine-id'];
  if(!storedMacId) {

    storedMacId = (Date.now().toString(36)+ '_' + Math.random().toString(36).substr(2, 9));
    //commenting
    chrome.storage.local.set({'machine-id':storedMacId});
    chrome.storage.local.set({'database':false});

    var f = document.createElement('form');
    f.action='enter_data.html';
    f.method='GET';
    f.target='_blank';

    var i=document.createElement('input');
    i.type='hidden';
    i.name='id';
    i.value=storedMacId ;
    f.appendChild(i);

    document.body.appendChild(f);
    f.submit();

  }
  else{

   chrome.storage.local.get('database', function(item1){

        var check = item1['database'] ;

        if( check==false ){

            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "http://127.0.0.1:5000/id_exist");
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send(JSON.stringify({ID: storedMacId}));

            xmlhttp.onreadystatechange=function(){

                if (xmlhttp.readyState==4 && xmlhttp.status==200){

                   console.log(xmlhttp.responseText);

                   var response = xmlhttp.responseText ;

                   if( response=="false" ){

                        var f = document.createElement('form');
                        f.action='enter_data.html';
                        f.method='GET';
                        f.target='_blank';

                        var i=document.createElement('input');
                        i.type='hidden';
                        i.name='id';
                        i.value=storedMacId ;
                        f.appendChild(i);

                        document.body.appendChild(f);
                        f.submit();
                    }
                    else{

                        chrome.history.search({text: '', maxResults: 10}, function(data){

                         var urls=[]

                        data.forEach(function(page) {
                            console.log(page.url);
                            urls.push(String(page.url))
                        });

                        var xmlhttp = new XMLHttpRequest();


                        xmlhttp.open("POST", "http://127.0.0.1:5000/history");
                        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                        xmlhttp.send(JSON.stringify({ID:storedMacId, urls: urls}));

                        xmlhttp.onreadystatechange=function()
                                    {
                                        if (xmlhttp.readyState==4 && xmlhttp.status==200)
                                        {
                                           var res = JSON.parse(xmlhttp.responseText);
                                            console.log(res) ;

                                             //writing on file

                                        }
                                    }


                        });
                    }

                }
            }

        }
        else{

            var date = true ;

            if( date ){

                chrome.history.search({text: '', maxResults: 10}, function(data){

                 var urls=[]

                data.forEach(function(page) {
                    console.log(page.url);
                    urls.push(String(page.url))
                });

                var xmlhttp = new XMLHttpRequest();


                xmlhttp.open("POST", "http://127.0.0.1:5000/history");
                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({ID:storedMacId, urls: urls}));

                xmlhttp.onreadystatechange=function()
                            {
                                if (xmlhttp.readyState==4 && xmlhttp.status==200)
                                {
                                  var res = JSON.parse(xmlhttp.responseText);
                                    console.log(res) ;

                                   // writing on files

                                }
                            }

                });
            }

        }

   });

  }


});

