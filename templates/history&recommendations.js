chrome.storage.local.get('background', function (img) {
    if (img['background'] == undefined) {
        chrome.storage.local.set({'background': "../img/nature.jpg"});
        change_background("../img/nature.jpg");
    } else {
        change_background(img['background']);
    }
});

function change_background(url) {
    document.getElementsByTagName("BODY")[0].style.backgroundImage = "url(" + url + ")";
    chrome.storage.local.set({'background': url});
}

showResults();
function showResults() {
    chrome.storage.local.get('res', function (results) {
            if (results['res']) {
                for (var k = 1; k <= results['res'].length; k++) {
                    i = results['res'][k - 1];
                    var ind = [];
                    for (var j = 0; j < i.length; j++) {
                        ind.push(j);
                    }
                    var ul = document.getElementById("res" + k);
                    ul.innerHTML = ""
                    for (var j = 0; j < Math.min(5, i.length); j++) {
                        var chosen = Math.floor(Math.random() * ind.length)
                        var li = document.createElement("li");
                        var a = document.createElement("a");
                        a.appendChild(document.createTextNode(i[ind[chosen]]));
                        a.setAttribute("href", i[ind[chosen]]);
                        a.setAttribute("class", "card-link");

                        li.appendChild(a);
                        ul.appendChild(li);
                        ind.splice(chosen, 1);
                    }
                    document.getElementById("content").style.visibility = "visible";
                }
            }
            else {
                //show defult res
            }
        }
    );
}
chrome.storage.local.get('machine-id', function (item) {
    var storedMacId = item['machine-id'];
    if (!storedMacId) {
        storedMacId = (Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9));
        //commenting
        chrome.storage.local.set({'machine-id': storedMacId});
        chrome.storage.local.set({'database': false});

        creatRegisterForm(storedMacId);
    }
    else {
        chrome.storage.local.get('database', function (item1) {
            var check = item1['database'];
            console.log(check);
            if (check == false) {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.open("POST", "http://127.0.0.1:5000/id_exist");
                xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xmlhttp.send(JSON.stringify({ID: storedMacId}));

                xmlhttp.onreadystatechange = function () {

                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                        console.log(xmlhttp.responseText);
                        var response = xmlhttp.responseText;

                        if (response == "false") {
                            creatRegisterForm(storedMacId);
                        }
                        else {
                            chrome.storage.local.set({'database': true});
                            sendHistory(storedMacId, 10);
                        }
                    }
                }
            }
            else {
                chrome.storage.local.get('lastUpdate', function (x) {

                    var oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
                    //console.log(x['lastUpdate'])
                    var today = new Date();
                    var firstDate = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
                    var secondDate = new Date(x['lastUpdate']['year'], x['lastUpdate']['month'], x['lastUpdate']['day']);

                    var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime()) / (oneDay)));
                    console.log(diffDays)

                    if (diffDays >= 4) {// number of days after we shod run clustring algorithem
                        sendHistory(storedMacId, 10);
                        showResults();
                    }
                });
            }
        });
    }
});

var refresh = document.getElementsByClassName("refresh");
for (var k = 0; k < refresh.length; k++) {
    (function (k) {
        refresh[k].addEventListener('click', function (event) {
            chrome.storage.local.get('res', function (results) {
                if (results['res']) {
                    i = results['res'][k];
                    var ind = [];
                    for (var j = 0; j < i.length; j++) {
                        ind.push(j);
                    }
                    var ul = document.getElementById("res" + (k + 1));
                    ul.innerHTML = "";
                    for (var j = 0; j < Math.min(5, i.length); j++) {
                        var chosen = Math.floor(Math.random() * ind.length)
                        var li = document.createElement("li");
                        var a = document.createElement("a");
                        a.appendChild(document.createTextNode(i[ind[chosen]]));
                        a.setAttribute("href", i[ind[chosen]]);
                        a.setAttribute("class", "card-link");

                        li.appendChild(a);
                        ul.appendChild(li);
                        ind.splice(chosen, 1);
                    }
                    document.getElementById("content").style.visibility = "visible";
                }
            });
        }, false);

    })(k);


}
function delete_saved_page(index) {
    chrome.storage.local.get('offlinePages', function (pages) {
        if (pages['offlinePages']) {
            pages['offlinePages'].splice(index, 1);
            chrome.storage.local.set({'offlinePages': pages['offlinePages']});
        }
        var link = document.getElementById('offline');
        if (link == undefined)
            return;
        link.innerHTML = "";
        for (var i = 0; i < pages['offlinePages'].length; i++) {
            link.innerHTML += "<li> <a href='#' id='" + i + "'>" + pages['offlinePages'][i]['title'] + "</a> <button id='delete" + i + "' class='btn-danger' style='float: right;font-size: 10px'>X</button> </li>";
        }
        for (i = 0; i < pages['offlinePages'].length; i++) {
            (function (i) {
                document.getElementById(i).addEventListener('click', function (event) {
                    var winPrint = window.open();
                    winPrint.document.write(pages['offlinePages'][i]['html']);
                    winPrint.document.close();
                    winPrint.focus();
                }, false);
                document.getElementById("delete" + i).addEventListener('click', function (event) {
                    delete_saved_page(i);
                }, false);

            })(i);
        }
    });
}

function sendHistory(storedMacId, numOfLinks) {
    chrome.history.search({text: '', maxResults: numOfLinks}, function (data) {
        var urls = []
        data.forEach(function (page) {
            console.log(page.url);
            urls.push(String(page.url))
        });

        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", "http://127.0.0.1:5000/history");
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({ID: storedMacId, urls: urls}));
//        var today = new Date();
//        chrome.storage.local.set({'lastUpdate':{'day':today.getDate(),'month':today.getMonth()+1,"year":today.getFullYear()}});

        xmlhttp.onreadystatechange = function () {

            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var res = JSON.parse(xmlhttp.responseText);
                console.log(res);

                //writing on file
                chrome.storage.local.set({'res': res});
                var today = new Date();
                chrome.storage.local.set({
                    'lastUpdate': {
                        'day': today.getDate(),
                        'month': today.getMonth() + 1,
                        "year": today.getFullYear()
                    }
                });
            }
        }
    });
}

chrome.storage.local.get('offlinePages', function (pages) {
        if (pages['offlinePages']) {
            for (var i = 0; i < pages['offlinePages'].length; i++) {
                var link = document.getElementById('offline');
                if (link == undefined)
                    return;
                link.innerHTML += "<li> <a href='#' id='" + i + "'>" + pages['offlinePages'][i]['title'] + "</a> <button id='delete" + i + "' class='btn-danger' style='float: right;font-size: 10px'>X</button> </li>";
            }
            for (i = 0; i < pages['offlinePages'].length; i++) {
                (function (i) {
                    document.getElementById(i).addEventListener('click', function (event) {
                        var winPrint = window.open();
                        winPrint.document.write(pages['offlinePages'][i]['html']);
                        winPrint.document.close();
                        winPrint.focus();
                    }, false);
                    document.getElementById("delete" + i).addEventListener('click', function (event) {
                        delete_saved_page(i);
                    }, false);

                })(i);
            }
        }
    }
);

document.getElementById('upload-image').addEventListener('change', readURL, true);
function readURL() {
    var file = document.getElementById("upload-image").files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
        change_background(reader.result);
    };
    if (file) {
        reader.readAsDataURL(file);
    } else {
    }
}

function creatRegisterForm(storedMacId) {
    var f = document.createElement('form');
    f.action = 'enter_data.html';
    f.method = 'GET';
    f.target = '_blank';
    var i = document.createElement('input');
    i.type = 'hidden';
    i.name = 'id';
    i.value = storedMacId;
    f.appendChild(i);
    document.body.appendChild(f);
    f.submit();
}
