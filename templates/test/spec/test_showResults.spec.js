
describe('Show Results',function(){

    it("Show Results from chrome local storage", function(done) {

        var theWindow = window.open('form.html'),
        theScript = document.createElement('script');
        theScript.src="testShowResults.js";

        theWindow.onload = function () {
            this.document.body.appendChild(theScript);
        };
        setTimeout(function() {
             expect(document.getElementById("showResults").value).toContain('true');
        done();
        },9000);
    },10000);

});