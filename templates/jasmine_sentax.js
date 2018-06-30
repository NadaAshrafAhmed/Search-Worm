describe("Using callbacks", function() {

    beforeEach(function(done) {
      setTimeout(function() {
        value = 0;
        done();
      }, 1);
    });

    it("should support async execution of test preparation and expectations", function(done) {
      value++;
      expect(value).toBeGreaterThan(0);
      done();
    });

    describe("A spec using done.fail", function() {
      var foo = function(x, callBack1, callBack2) {
        if (x) {
          setTimeout(callBack1, 0);
        } else {
          setTimeout(callBack2, 0);
        }
      };

      it("should not call the second callBack", function(done) {
        foo(true,
          done,
          function() {
            done.fail("Second callback has been called");
          }
        );
      });
    });
  });
describe("Using promises", function() {
    if (!browserHasPromises()) {
      return;
    }

    beforeEach(function() {
      return soon().then(function() {
        value = 0;
      });
    });

    it("should support async execution of test preparation and expectations", function() {
      return soon().then(function() {
        value++;
        expect(value).toBeGreaterThan(0);
      });
    });
  });
describe("Using async/await", function() {
    if (!browserHasAsyncAwaitSupport()) {
      return;
    }

    beforeEach(async function() {
      await soon();
      value = 0;
    });

    it("should support async execution of test preparation and expectations", async function() {
      await soon();
      value++;
      expect(value).toBeGreaterThan(0);
    });
  });
describe("long asynchronous specs", function() {
    beforeEach(function(done) {
      done();
    }, 1000);

    it("takes a long time", function(done) {
      setTimeout(function() {
        done();
      }, 9000);
    }, 10000);

    afterEach(function(done) {
      done();
    }, 1000);
  });

  function soon() {
    return new Promise(function(resolve, reject) {
      setTimeout(function() {
        resolve();
      }, 1);
    });
  }

  function browserHasPromises() {
    return typeof Promise !== 'undefined';
  }

  function getAsyncCtor() {
    try {
      eval("var func = async function(){};");
    } catch (e) {
      return null;
    }

    return Object.getPrototypeOf(func).constructor;
  }

  function browserHasAsyncAwaitSupport() {
    return getAsyncCtor() !== null;
  }
});