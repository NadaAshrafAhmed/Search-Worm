function downloadPage(tablink,fun)
{
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
                            fun("Delete Page")
//                            link.innerHTML = "Delete Page";
                        } else {
                            fun("Error!")
//                            link.innerHTML = "Error!";
                        }
                    }
                };
            });
        }
    });
}