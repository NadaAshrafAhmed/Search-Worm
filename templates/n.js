chrome.storage.local.get('background', function (img) {
    if (img['background'] == undefined) {
        chrome.storage.local.set({'background': "../img/nature.jpg"});
        change_background("../img/nature.jpg");
    }else {
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

chrome.storage.local.get('offlinePages', function (pages) {
        var downloaded = false;
        if (pages['offlinePages']) {
            for (var i = 0; i < pages['offlinePages'].length; i++) {
                var link = document.getElementById('dropdown');
                if (link == undefined)
                    return;
                link.innerHTML += "<a id='" + i + "'>" + pages['offlinePages'][i]['url'] + "</a>";
            }
            for (i = 0; i < pages['offlinePages'].length; i++) {
                (function (i) {
                    document.getElementById(i).addEventListener('click', function (event) {
                        var winPrint = window.open();
                        winPrint.document.write(pages['offlinePages'][i]['html']);
                        winPrint.document.close();
                        winPrint.focus();
                    }, false);
                })(i);
            }
        }
    }
);

chrome.storage.local.get('offlinePages', function (pages) {
    console.log(pages['offlinePages']);
});

function save_remove(tablink) {
    var link = document.getElementById('download');
    if (link == undefined)
        return;
    if (link.innerHTML == "Save Page") {
        link.innerHTML = "Saving...";
        console.log("download");
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
                            console.log(res);
                            if (res != "") {
                                pages['offlinePages'].push({
                                    'url': tablink,
                                    'html': res
                                });
                                chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                                var id = pages['offlinePages'].length - 1;
                                console.log(id);
                                document.getElementById('dropdown').innerHTML += "<a id='" + id + "'>" + tablink + "</a>";
                                link.innerHTML = "Delete Page";
                                for (i = 0; i < pages['offlinePages'].length; i++) {
                                    (function (i) {
                                        document.getElementById(i).addEventListener('click', function (event) {
                                            var winPrint = window.open();
                                            winPrint.document.write(pages['offlinePages'][i]['html']);
                                            winPrint.document.close();
                                            winPrint.focus();
                                        }, false);
                                    })(i);
                                }

                            } else {
                                link.innerHTML = "Saving Page";
                            }
                        }
                    };
                });
            }
        });
    }

    if (link.innerHTML == "Delete Page") {
        console.log('remove');
        chrome.storage.local.get('offlinePages', function (pages) {
            if (pages['offlinePages']) {
                for (var i = 0; i < pages['offlinePages'].length; i++) {
                    if (pages['offlinePages'][i]['url'] == tablink) {
                        pages['offlinePages'].splice(i, 1);
                        chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                        document.getElementById('download').innerHTML = "Delete Page";
                        console.log(pages['offlinePages']);
                        link.innerHTML = "Save Page";

                        document.getElementById('dropdown').innerHTML = "";

                        for (var j = 0; j < pages['offlinePages'].length; j++) {
                            document.getElementById('dropdown').innerHTML += "<a id='" + j + "'>" + pages['offlinePages'][j]['url'] + "</a>";
                        }
                        for (i = 0; i < pages['offlinePages'].length; i++) {
                            (function (i) {
                                document.getElementById(i).addEventListener('click', function (event) {
                                    var winPrint = window.open();
                                    winPrint.document.write(pages['offlinePages'][i]['html']);
                                    winPrint.document.close();
                                    winPrint.focus();
                                }, false);
                            })(i);
                        }
                        break;
                    }
                }
            }
        });
    }
}
function download(tablink) {

    console.log("download");
    chrome.storage.local.get('offlinePages', function (pages) {

        if (pages['offlinePages']) {
//                var x=pages['offlinePages'];
            pages['offlinePages'].push({
                'url': tablink,
                'html': "<html><body><a href='" + tablink + "'>page</a></body></html>"
            });
            chrome.storage.local.set({'offlinePages': pages['offlinePages']});
            console.log(pages['offlinePages']);
            convert(tablink);
        }

    });

}
function remove(tablink) {

    console.log('remove');
    chrome.storage.local.get('offlinePages', function (pages) {
        if (pages['offlinePages']) {
            for (var i = 0; i < pages['offlinePages'].length; i++) {
                if (pages['offlinePages'][i]['url'] == tablink) {
                    pages['offlinePages'].splice(i, 1);
                    chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                    document.getElementById('download').innerHTML = "Delete Page";
                    console.log(pages['offlinePages']);
                    convert(tablink);
                    break;
                }
            }
        }
    });

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


var dropdown = document.getElementsByClassName("dropdown-btn");
if (dropdown != undefined) {
    var i;
    for (i = 0; i < dropdown.length; i++) {
        dropdown[i].addEventListener("click", function () {
            this.classList.toggle("active");
            var dropdownContent = this.nextElementSibling;
            if (dropdownContent.style.display === "block") {
                dropdownContent.style.display = "none";
            } else {
                dropdownContent.style.display = "block";
            }
        });
    }
}