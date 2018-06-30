describe('Save page',function(){

    it("download correct url ", function(done) {
        var  downloadPageReturn,downloaded,url;
        url="https://stackoverflow.com/questions/2869827/how-to-test-chrome-extensions";
        downloadPage(url,function(txt)
        {
            downloadPageReturn=txt;
            console.log(txt);
            chrome.storage.local.get('offlinePages', function (pages) {
                downloaded = false;
                if (pages['offlinePages']) {
                    console.log(pages['offlinePages']);
                    for (var i = 0; i < pages['offlinePages'].length; i++) {
                        if (pages['offlinePages'][i]['url'] == url) {
                            downloaded = true;
                            pages['offlinePages'].splice(i, 1);
                            chrome.storage.local.set({'offlinePages':pages['offlinePages']});

                            break;
                        }
                    }
                }
            });
        });

      setTimeout(function() {
        expect(downloadPageReturn).toBe("Delete Page");
        expect(downloaded).toBe(true);
        done();
      }, 19000);
    },20000);

    it("download uncorrect url ", function(done) {
        var  downloadPageReturn,downloaded,url;
        url="https://stackover.com";
        downloadPage(url,function(txt)
        {
            downloadPageReturn=txt;
            chrome.storage.local.get('offlinePages', function (pages) {
                downloaded = false;
                if (pages['offlinePages']) {
                    for (var i = 0; i < pages['offlinePages'].length; i++) {
                        if (pages['offlinePages'][i]['url'] == url) {
                            downloaded = true;
                            pages['offlinePages'].splice(i, 1);
                            chrome.storage.local.set({'offlinePages':pages['offlinePages']});
                            break;
                        }
                    }
                }
            });
        });

      setTimeout(function() {
        expect(downloadPageReturn).toBe("Error!");
        expect(downloaded).toBe(false);
        done();
      }, 9000);
    },10000);



});