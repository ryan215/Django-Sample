'use strict';

define(['app'], function(app) {

	app.register.controller('registrationCtrl', ['$scope',
        function ($scope) {

    }]);


    app.register.service('specialtyTags', function ($q, $rootScope) {
        $rootScope.q = $q
    });


	app.register.controller('registrationController', ["localStorageService",'$stateParams',"$resource","$http","$scope","rest","specialtyTags",
		function(localStorageService,$stateParams,$resource,$http,$scope) {

			//test
			// Stripe.setPublishableKey("pk_test_xO4m1cYHr0GCBYbSH2GxdXp8");
			//live
			Stripe.setPublishableKey("pk_live_oO497oIjwqYyvE443zBQYrmw");

			$scope.step = 'registration';
			$scope.urlTier = $stateParams.tier;
			$scope.urlPro = $stateParams.pro;
			$scope.temTags = [];

    		$scope.user = {
				first_name: '',
				last_name: '',
				email: '',
				password: '',
				password2: '',
				gender: '',
				referred_by: localStorageService.get('referral'),
				tags: [],
				tier: 1
			};
			$scope.pro = {
				profession: '',
				education: '',
				experience: '',
				certification_name1: '',
				certification_number1: '',
				certification_name2: '',
				certification_number2: '',
				phone: '',
				twitter: '',
			    facebook: '',
			    instagram: '',
			    youtube: '',
			    linkedin: '',
			    plus: ''
			};
			$scope.address = {
				street_line1: '',
				street_line2: '',
				city: '',
				state: '',
				country: '',
				zipcode: '',
				lat: '',
				lng: ''
			};
			$scope.creditcard = {
				name : '',
				number : '',
				cvc : '',
				exp_month : '',
				exp_year : '',
				address_line1 : "",
				address_line2 : "",
				address_city : "",
				address_country : "",
				address_state : "",
				address_zip : "",
    		};
    		$scope.choices = [{"id":1, "value":"1", "label":"Good"}, {"id":2, "value":"2","label":"Ok"},{"id":3, "value":"3","label":"Bad"}];
    $scope.value = [];
    $scope.updateQuestionValue = function(choice){
        $scope.value = $scope.value || [];
        if(choice.checked){
            $scope.value.push(choice.value);
            $scope.value = _.uniq($scope.value);
        }else{
            $scope.value = _.without($scope.value, choice.value);
        }
    };


    		var AuthToken =  $resource(":protocol://:url/accounts/register/", {
    			protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            var ProAuthToken =  $resource(":protocol://:url/accounts/register-professional/", {
            	protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            var paymentResource = $resource(":protocol://:url/users/modify-payment-details/:id",{
            	id : '@id',
            	protocol: $scope.restProtocol,
            	url: $scope.restURL,
            },{update: { method: 'PUT' }});
            var tagsResource = $resource(":protocol://:url/tags/",{
            	protocol: $scope.restProtocol,
            	url: $scope.restURL,
            },{update: { method: 'PUT' }});


            $scope.tagsCall = tagsResource.get($scope.user, function(){
            	$scope.temTags = $scope.tagsCall.results;

			},function(error) {
				$scope.message = error.data;
			});


            $scope.tags = [];
            $scope.addTagBank = function(tag) {
            	if($scope.tags.indexOf(tag) == -1){
            		$scope.tags.push(tag);
            		$scope.user.tags.push(tag.name);
            	}
            };
            $scope.onTagAdd = function (tag) {
                $scope.user.tags.push(tag.name);
            };
            $scope.onDeleteTag = function (tag) {
            	var temp = $scope.user.tags.indexOf(tag.name);
            	$scope.user.tags.splice(temp, 1);
            };
            $scope.loadSpecialty = function () {
                var deferred = $scope.q.defer();
                deferred.resolve($scope.temTags);
                return deferred.promise;
            };
			$scope.getCurrentStep = function() {
				return $scope.step;
			};
			$scope.setCurrentStep = function(step){
				$scope.step = step;
			};
			$scope.setCurrentStepFormPar = function(step, valid){
				if($scope.urlTier == 7 && $scope.urlPro !== undefined && $scope.urlPro != ''){
					if($scope.urlPro == 'Trainer' || $scope.urlPro == 'Nutritionist' || $scope.urlPro == 'Promoter' || $scope.urlPro == 'Instructor' ){
						$scope.user.tier = $scope.urlTier;
						$scope.pro.profession = $scope.urlPro;
						if(valid == true){
							$scope.step = 'professionals';
						};
					};
				}
				else if($scope.urlTier >= 1 && $scope.urlTier <= 5){
					$scope.user.tier = $scope.urlTier;
					if(valid == true){
						$scope.step = 'membershipSubmit';
					};
				}
				else{
					if(valid == true){
						$scope.step = 'choice';
					};
				};
			};
			$scope.setCurrentStepForm = function(step, valid){
				if(valid == true){$scope.step = step;};
			};
			$scope.membership = function(step, tier){
				$scope.user.tier = tier;
				$scope.step = step;
			};
			$scope.professionals = function(step, tier, pro){
				$scope.pro.profession = pro;
				$scope.user.tier = tier;
				$scope.step = step;
			};
			$scope.ifPromoter = function(){
				if($scope.pro.profession == 'Promoter'){
					return false;
				}
				else{
					return true;
				};
			};
			$scope.paymentCheck = function(step, valid){
				$scope.stripeToken;
				if(valid == true){

	                Stripe.createToken({
	                    name: $scope.creditcard.name,
	                    number: $scope.creditcard.number,
	                    cvc: $scope.creditcard.cvc,
	                    exp_month: $scope.creditcard.exp_month,
	                    exp_year: $scope.creditcard.exp_year,
	                    address_line1: $scope.creditcard.address_line1,
	                    address_line2: $scope.creditcard.address_line2,
	                    address_city: $scope.creditcard.address_city,
	                    address_country: $scope.creditcard.address_country,
	                    address_state: $scope.creditcard.address_state,
	                    address_zip: $scope.creditcard.address_zip,
	                }, function (status, response) {
	                    if (response.error) {
	                        $scope.message = [response.error.message];
	                        $scope.$apply();
	                    }
	                    else {
	                    	$scope.message = null;
	                    	$scope.stripeToken = response['id'];
	                    	$scope.step = step;
	                    	$scope.$apply();
	                    };
	                });

				};
			};
			$scope.preSubmit = function(){
				$scope.user.primary_address = $scope.address;
				$scope.submit();
			};
			$scope.preProSubmit = function(){
				angular.forEach($scope.user, function(value, key){
					$scope.pro[key] = value;
				});
				$scope.pro.primary_address = $scope.address;
				$scope.proSubmit();
			};



			$scope.submit = function(){
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

				$scope.authToken = AuthToken.save($scope.user, function(){
					localStorageService.add('Authorization', 'Token ' + $scope.authToken.token);
					localStorageService.add('rest_token', $scope.authToken.token);
					localStorageService.add('user_id', $scope.authToken.id);
					localStorageService.add('user_email', $scope.authToken.email);
                    localStorageService.add('user_img', $scope.authToken.img);
                    localStorageService.add('user_type', $scope.authToken.type);
                    if($scope.user.tier == 1){
						window.location = "/";
					}
					else{
						$scope.profile_user = $scope.authToken.id;
						$http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');
						$scope.responsePayment = paymentResource.update({id:$scope.profile_user},{id:$scope.profile_user,stripeToken:$scope.stripeToken}, function(){
							window.location = "/";
						});
						delete $http.defaults.headers.common['Authorization'];

					};
				},function(error) {
					$scope.message = error.data;
				});
			};

			$scope.proSubmit = function(){
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

				$scope.authToken = AuthToken.save($scope.pro, function(){
					localStorageService.add('Authorization', 'Token ' + $scope.authToken.token);
					localStorageService.add('rest_token', $scope.authToken.token);
					localStorageService.add('user_id', $scope.authToken.id);
					localStorageService.add('user_email', $scope.authToken.email);
                    localStorageService.add('user_img', $scope.authToken.img);
                    localStorageService.add('user_type', $scope.authToken.type);

                    $scope.proToken = ProAuthToken.save($scope.pro, function(){

                    	window.location = "/";

                    	// $scope.profile_user = $scope.authToken.id;
						// $http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');
						// $scope.responsePayment = paymentResource.update({id:$scope.profile_user},{id:$scope.profile_user,stripeToken:$scope.stripeToken}, function(){
						// 	window.location = "/";
						// });
						// delete $http.defaults.headers.common['Authorization'];

					},function(error) {
						$scope.message = error.data;
					});

				},function(error) {
					$scope.message = error.data;
				});
			}



			//Set Adress From Google GeoLocation
			$scope.tempAddress = {
				formatted_address:'',
				street_line2:'',
			};
			$scope.setAddress = function() {
				if ($scope.tempAddress.formatted_address !== "undefined")
				{
					$scope.address = $scope.addressesInputs[$scope.tempAddress.formatted_address];
					if ($scope.address !== undefined){
						$scope.address.street_line2 = (!($scope.tempAddress.street_line2 === undefined)?$scope.tempAddress.street_line2 + ' ':'');
					}
				}
			};
			$scope.tempAddressPay = {
				formatted_address:'',
				street_line2:'',
			};
			$scope.setAddressPay = function() {
				if ($scope.tempAddressPay.formatted_address !== "undefined")
				{
					$scope.creditcard.address_line1 = (!($scope.addressesInputs[$scope.tempAddressPay.formatted_address] === undefined)?$scope.addressesInputs[$scope.tempAddressPay.formatted_address].street_line1 + ' ':'');
					$scope.creditcard.address_city = (!($scope.addressesInputs[$scope.tempAddressPay.formatted_address] === undefined)?$scope.addressesInputs[$scope.tempAddressPay.formatted_address].city + ' ':'');
					$scope.creditcard.address_country = (!($scope.addressesInputs[$scope.tempAddressPay.formatted_address] === undefined)?$scope.addressesInputs[$scope.tempAddressPay.formatted_address].country + ' ':'');
					$scope.creditcard.address_state = (!($scope.addressesInputs[$scope.tempAddressPay.formatted_address] === undefined)?$scope.addressesInputs[$scope.tempAddressPay.formatted_address].state + ' ':'');
					$scope.creditcard.address_zip = (!($scope.addressesInputs[$scope.tempAddressPay.formatted_address] === undefined)?$scope.addressesInputs[$scope.tempAddressPay.formatted_address].zipcode + ' ':'');

					if ($scope.creditcard !== undefined){
						$scope.creditcard.address_line2 = (!($scope.tempAddressPay.street_line2 === undefined)?$scope.tempAddressPay.street_line2 + ' ':'');
					}
				}
			};

			//$Google GeoLocation
			$scope.addressesInputs = {};
			$scope.getLocation = function(val) {
				delete $http.defaults.headers.common['Authorization']
				return $http.get('https://maps.googleapis.com/maps/api/geocode/json', {
					params: {
				    address: val,
				    sensor: false,
				    components:'country:USA'
					}
				}).then(function(res){
					$scope.addressesInputs = {};
					var addresses = [];
					var types = {};
					angular.forEach(res.data.results, function(item){
						for (var i = 0; i < item.address_components.length; i++) {
                            var addressType = item.address_components[i].types[0];
                            types[addressType] = i;
                        };
						addresses.push(item.formatted_address);
						for (var i = 0; i < item.address_components.length; i++) {
							$scope.addressesInputs[item.formatted_address] = {
								street_line1: (!(types['street_number'] === undefined)?item.address_components[types['street_number']]['short_name'] + ' ':'') + (!(types['route'] === undefined)?item.address_components[types['route']]['long_name'] + ' ':''),
								city: (!(types['locality'] === undefined)?item.address_components[types['locality']]['short_name']:!(types['sublocality'] === undefined)?item.address_components[types['sublocality']]['short_name']:!(types['neighborhood'] === undefined)?item.address_components[types['neighborhood']]['short_name'] + ' ':''),
								state: (!(types['administrative_area_level_1'] === undefined)?item.address_components[types['administrative_area_level_1']]['short_name'] + ' ':''),
								country: (!(types['country'] === undefined)?item.address_components[types['country']]['long_name'] + ' ':''),
								zipcode: (!(types['postal_code'] === undefined || item.address_components[types['postal_code']] === undefined)?item.address_components[types['postal_code']]['short_name']:''),
								lat: item.geometry.location.lat,
								lng: item.geometry.location.lng
							};
						};
					});
					$http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');
					return addresses;
				});
			};


	}]);



});
