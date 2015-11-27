var url = require("url");

describe('angular', function() {
    var ptor = protractor.getInstance();
    ptor.ignoreSynchronization = true;

    //This function  replaces "ptor.get", because "prot.get" will not wait for manual bootstrapping.
    //This function adds 0.5 sec wait before checking that the url has been set correctly.
    function ptor_get(rel_path, pause_by) {
        ptor.driver.get(url.resolve(ptor.baseUrl, rel_path));
        ptor.wait(function () {
            if (pause_by) {
                waits(pause_by);
            }
            return ptor.driver.getCurrentUrl().then(function(in_url) {
                var re = new RegExp(rel_path, "i");
                return re.test(in_url);
            });
        }, 5000, "Taking too long to load " + rel_path);
    }


    describe("Home-", function () {

        it('Testing URL', function() {
            ptor_get('#/',5000);
            ptor.sleep(500)
            expect(ptor.getCurrentUrl()).toContain('');
        });

    });

    describe("Testing Buttons LoggedOut-", function () {

        it('Testing About Page', function() {
            element(by.id('about')).click();
            expect(ptor.getCurrentUrl()).toContain('about');
            ptor.sleep(2000)
        });

        it('Testing Home Page', function() {
            element(by.id('home')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

        it('Testing About Page Again', function() {
            element(by.id('about')).click();
            expect(ptor.getCurrentUrl()).toContain('about');
            ptor.sleep(2000)
        });

        it('Testing Home Logo Page', function() {
            element(by.id('home-logo')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

    });


    describe("Login-", function () {

        it('Input Creadentials', function() {
            element(by.id('login-tab')).click();
            ptor.sleep(2000)
            element(by.id('login')).click();
            ptor.sleep(2000)
            element(by.model('user.email')).sendKeys('admin@test.com');
            element(by.model('user.password')).sendKeys('admin123');
            element(by.id('signin')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)

        });

    });


    describe("Testing Buttons LoggedIn-", function () {

        it('Testing Demo Page', function() {
            element(by.id('demo')).click();
            expect(ptor.getCurrentUrl()).toContain('demo');
            ptor.sleep(2000)
        });

        it('Testing Home Page', function() {
            element(by.id('home')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

        it('Testing Demo Page Again', function() {
            element(by.id('demo')).click();
            expect(ptor.getCurrentUrl()).toContain('demo');
            ptor.sleep(2000)
        });

        it('Testing Home Logo Page', function() {
            element(by.id('home-logo')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

    });



    describe("LogOut-", function () {

        it('Logging out', function() {
            element(by.id('account-tab')).click();
            ptor.sleep(2000)
            element(by.id('logout')).click();
            ptor.sleep(2000)

        });

    });


    describe("Register", function () {

        it('Logging out', function() {
            var temp_name = Math.floor((Math.random()*100)+1);
            element(by.id('register')).click();
            ptor.sleep(2000)
            element(by.model('user.first_name')).sendKeys('Jonh');
            element(by.model('user.last_name')).sendKeys('Doe');
            element(by.model('user.email')).sendKeys(temp_name + '@test.com');
            element(by.model('user.password')).sendKeys('12345678');
            element(by.model('user.password2')).sendKeys('12345678');
            ptor.sleep(2000)
            element(by.id('signin')).click();
            ptor.sleep(2000)

        });

    });


    describe("Testing Buttons LoggedIn-", function () {

        it('Testing Demo Page', function() {
            element(by.id('demo')).click();
            expect(ptor.getCurrentUrl()).toContain('demo');
            ptor.sleep(2000)
        });

        it('Testing Home Page', function() {
            element(by.id('home')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

        it('Testing Demo Page Again', function() {
            element(by.id('demo')).click();
            expect(ptor.getCurrentUrl()).toContain('demo');
            ptor.sleep(2000)
        });

        it('Testing Home Logo Page', function() {
            element(by.id('home-logo')).click();
            expect(ptor.getCurrentUrl()).toContain('');
            ptor.sleep(2000)
        });

    });



    describe("LogOut-", function () {

        it('Logging out', function() {
            element(by.id('account-tab')).click();
            ptor.sleep(2000)
            element(by.id('logout')).click();
            ptor.sleep(2000)

        });

    });

});
