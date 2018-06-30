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
                                console.log("Getting Title ... ");
                                var x ="";
                                var y = res.indexOf("</title>") - 1;
                                while (res[y] != '>') {
                                    x += res[y];
                                    y -= 1;
                                }
                                x = x.split("").reverse().join("");
                                pages['offlinePages'].push({
                                    'url': tablink,
                                    'html': res,
                                    'title': x
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

