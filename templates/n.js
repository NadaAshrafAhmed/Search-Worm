if (document.getElementById('upload-image') != undefined) {
    chrome.storage.local.get('background', function (img) {
        if (img['background'] == undefined) {
            chrome.storage.local.set({'background': "../img/nature.jpg"});
            change_background("../img/nature.jpg");
        } else {
            change_background(img['background']);
        }
    });

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

    function change_background(url) {
        document.getElementsByTagName("BODY")[0].style.backgroundImage = "url(" + url + ")";
        chrome.storage.local.set({'background': url});
    }
}
var refresh = document.getElementsByClassName("refresh");
for (var i = 0; i < refresh.length; i++) {
    refresh[i].addEventListener('click', function (event) {
        location.reload(false);
    }, false);
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
                        delete_saved(i);
                    }, false);

                })(i);
            }
        }
    }
);

function delete_saved(index) {
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
                    delete_saved(i);
                }, false);

            })(i);
        }
    });
}
chrome.storage.local.get('offlinePages', function (pages) {
    console.log(pages['offlinePages']);
});

function save_remove(tablink) {
    var link = document.getElementById('download');
    if (link == undefined)
        return;
    if (link.innerHTML == "Save Page") {
        link.innerHTML = "Saving";
        var dots = window.setInterval(function () {
            var wait = document.getElementById("download");
            if (wait.innerHTML.charAt(0) != 'S') {
                clearInterval(dots);
            } else if (wait.innerHTML.length > 9)
                wait.innerHTML = "Saving";
            else
                wait.innerHTML += ".";
        }, 200);

        console.log("downloading...");
        chrome.storage.local.get('offlinePages', function (pages) {
            if (pages['offlinePages']) {
                chrome.storage.local.get('machine-id', function (item) {
                    var xmlhttp = new XMLHttpRequest();
                    xmlhttp.open("POST", "http://127.0.0.1:5000/get_html");
                    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                    xmlhttp.send(JSON.stringify({ID: item['machine-id'], url: tablink}));

                    xmlhttp.onreadystatechange = function () {
                        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                            var res = xmlhttp.responseText;
                            if (res != "") {
                                // console.log(res);
                                var x = res.indexOf("<title>") + "<title>".length;
                                var y = res.indexOf("</title>") - 1;
                                var z = res.substring(x, y);
                                console.log(x + " " + y + ":(" + z + ")");
                                pages['offlinePages'].push({
                                    'url': tablink,
                                    'html': res,
                                    'title': z
                                });
                                chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                                link.innerHTML = "Delete Page";
                            } else {
                                link.innerHTML = "Error!";
                            }
                        }
                    };
                });
            }
        });
    } else if (link.innerHTML == "Delete Page") {
        console.log('deleting...');
        chrome.storage.local.get('offlinePages', function (pages) {
            if (pages['offlinePages']) {
                for (var i = 0; i < pages['offlinePages'].length; i++) {
                    if (pages['offlinePages'][i]['url'] == tablink) {
                        pages['offlinePages'].splice(i, 1);
                        chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                        // document.getElementById('download').innerHTML = "Delete Page";
                        // console.log(pages['offlinePages']);
                        link.innerHTML = "Save Page";
                        break;
                    }
                }
            }
        });
    }
}
chrome.tabs.getSelected(null, function (tab) {

    var tablink = tab.url;
    console.log(tablink);
    chrome.storage.local.get('offlinePages', function (pages) {
        var downloaded = false;
        if (pages['offlinePages']) {
            for (var i = 0; i < pages['offlinePages'].length; i++) {
                if (pages['offlinePages'][i]['url'] == tablink) {
                    var link = document.getElementById('download');
                    if (link == undefined)
                        return;
                    link.innerHTML = "Delete Page";
                    downloaded = true;
                    link.addEventListener('click', function () {
                        save_remove(tablink);
                    });
                    break;
                }
            }
        }
        else {
            chrome.storage.local.set({'offlinePages': []});
        }


        if (!downloaded) {
            var link = document.getElementById('download');
            if (link == undefined)
                return;
            link.innerHTML = "Save Page";
            link.addEventListener('click', function () {
                save_remove(tablink);
            });
        }
    });
});

