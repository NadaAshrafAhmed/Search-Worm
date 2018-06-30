
describe('Enter Data',function(){

    beforeAll(function(done) {
        tabs=[]
        chrome.storage.local.get('machine-id', function(item){
            id=item['machine-id'];
            if(item['machine-id'])
            {
            chrome.storage.local.remove('machine-id');
            }

        });

        chrome.storage.local.get('database', function(item){
            database=item['database'];
            if(item['database'])
            {
                chrome.storage.local.remove('database');
            }
        });
        done();
    }, 1000);

    afterAll(function(){
        chrome.storage.local.set({'machine-id':id});
        chrome.storage.local.set({'database':database});
        chrome.tabs.remove(tabs);
    });

    beforeEach(function(done) {
        done();
    }, 1000);


    it("New User", function(done) {

      setTimeout(function() {
      chrome.tabs.create({url: "form.html",active:true},function(tab) {
        tabs.push(tab.id);
      });
      },1000);
      setTimeout(function() {
        chrome.tabs.getSelected(null, function (tab) {
             expect(tab.url).toContain("enter_data.html");

             tabs.push(tab.id);
             done();
        });
      }, 2000);


    },3000);

    it("New User not submit data", function(done) {

      chrome.tabs.create({url: "form.html",active:true},function(tab) {
        tabs.push(tab.id);
      });
      setTimeout(function() {
        chrome.tabs.getSelected(null, function (tab) {
             tabs.push(tab.id);
             expect(tab.url).toContain("enter_data.html");
             chrome.tabs.create({url: "form.html"},function(tab) {
                tabs.push(tab.id);
              });
             setTimeout(function() {
                chrome.tabs.getSelected(null, function (tab) {
                     tabs.push(tab.id);
                     expect(tab.url).toContain("enter_data.html");

                });
              }, 1000);
             done();
        });
      }, 1000);


    },2000);

    it("New User submit data", function(done) {

        chrome.storage.local.set({'machine-id':"ll"});

        var theWindow = window.open('enter_data.html'),
        theScript = document.createElement('script');
        theScript.src="submitData.js";

        theWindow.onload = function () {
            this.document.body.appendChild(theScript);
        };
//        console.log(theWindow.id);
        setTimeout(function() {
            chrome.tabs.create({url: "form.html"},function(tab) {
                tabs.push(tab.id);
              });
        },5000);
        setTimeout(function() {
            chrome.tabs.getSelected(null, function (tab) {
                expect(tab.url).toContain("form.html");
                tabs.push(tab.id);
            });
            chrome.storage.local.get('database', function(item){
                if(item['database'])
                {
                    db=item['database'];
                }
            });
        },6000);
        setTimeout(function() {
             expect(db).toContain(true);
        done();
        },7000);
    },8000);

});