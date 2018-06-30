
describe('Delete page',function(){

    it("remove downloaded url ", function(done) {
        var  downloadPageReturn,deleted,url;
        url="https://stackoverflow.com/questions/2869827/how-to-test-chrome-extensions";
        downloadPage(url,function(txt)
        {
            downloadPageReturn=txt;
            if(txt=="Delete Page")
            {

                chrome.storage.local.get('offlinePages', function (pages) {
                    deleted = true;
                    if (pages['offlinePages']) {
                        for (var i = 0; i < pages['offlinePages'].length; i++) {
                            if (pages['offlinePages'][i]['url'] == url) {
                                deleted = false;
                                break;
                            }
                        }
                    }
                });
            }

        });

      setTimeout(function() {
        expect(downloadPageReturn).toBe("Delete Page");
        expect(deleted).toBe(false);
        done();
      }, 19000);
    },20000);


});