'use strict';

define(['app'], function(app) {

	app.register.controller('membershipCtrl', ['$scope', 'restricted',
        function ($scope) {
        	$scope.restricted();
    }]);


	app.register.controller('membershipController', ["localStorageService",'$stateParams',"$resource","$http","$scope","rest",
		function(localStorageService,$stateParams,$resource,$http,$scope) {

			//test
			// Stripe.setPublishableKey("pk_test_xO4m1cYHr0GCBYbSH2GxdXp8");
			//live
			Stripe.setPublishableKey("pk_live_oO497oIjwqYyvE443zBQYrmw");

			$scope.urlTier = $stateParams.tier;
			$scope.urlPro = $stateParams.pro;

			$scope.step = 'auth';
			$scope.auth = {
				email: '',
				password: ''
			};
			$scope.user = {
				id: localStorageService.get('user_id'),
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


    		var AuthToken =  $resource(":protocol://:url/membership/auth/", {
    			protocol: $scope.restProtocol,
                url: $scope.restURL
            });
    		var userResource = $resource(":protocol://:url/membership/upgrade-tier/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL
            },{update: { method: 'PUT' }});
            var professionalResource = $resource(":protocol://:url/membership/upgrade-pro/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL
            },{update: { method: 'PUT' }});
            var cancelResource = $resource(":protocol://:url/membership/cancel/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL
            },{update: { method: 'PUT' }});
            var paymentResource = $resource(":protocol://:url/users/modify-payment-details/:id",{
            	id : '@id',
            	protocol: $scope.restProtocol,
            	url: $scope.restURL,
            },{update: { method: 'PUT' }});
            var connectResource =  $resource(":protocol://:url/users/connect/:id/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL,
                id: "@id"
            },{update: { method: 'PUT' }});


            $scope.getCurrentStep = function() {
				return $scope.step;
			};
			$scope.setCurrentStep = function(step){
				$scope.step = step;
			};
            $scope.authenticate = function(step, valid) {
            	if(valid == true){
            		//AutoFill Fix
	                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

					$scope.authToken = AuthToken.save($scope.auth, function() {
						if($scope.authToken.email == localStorageService.get('user_email')){


							if($scope.urlTier == 7 && $scope.urlPro !== undefined && $scope.urlPro != ''){
								if($scope.urlPro == 'Trainer' || $scope.urlPro == 'Nutritionist' || $scope.urlPro == 'Promoter' || $scope.urlPro == 'Instructor' ){
									$scope.user.tier = $scope.urlTier;
									$scope.pro.profession = $scope.urlPro;
									$scope.step = 'professionals';
								};
							}
							else if($scope.urlTier >= 2 && $scope.urlTier <= 5){
								$scope.user.tier = $scope.urlTier;
								$scope.step = 'payment';
							}
							else if($scope.urlTier >= 'cancel'){
								$scope.step = 'cancel';
							}
							else{
								if(valid == true){
									$scope.step = step;
								};
							};

						};
					},function(error) {
						$scope.message = error.data;
					});
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
			$scope.preProSubmit = function(){
				angular.forEach($scope.user, function(value, key){
					$scope.pro[key] = value;
				});
				$scope.proSubmit();
			};



			$scope.submit = function(){
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

				$scope.userUpdate = userResource.save($scope.user, function() {
					localStorageService.add('user_type', $scope.userUpdate.details);
					$scope.profile_user = localStorageService.get('user_id');
					$scope.pro_user = localStorageService.get('profesional');
					$scope.responsePayment = paymentResource.update({id:$scope.profile_user},{id:$scope.profile_user,stripeToken:$scope.stripeToken}, function(){
						if($scope.pro_user != null){
							$scope.connect = connectResource.update({id: $scope.profile_user, professional_id: $scope.pro_user},
								function (data) {
									localStorageService.remove('profesional');
									window.location = "/";
	                        });
						}
						else{
							window.location = "/";
						}
					});
				},function(error) {
					$scope.message = error.data;
				});

			};
			$scope.proSubmit = function(){
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

				$scope.proUpdate = professionalResource.save($scope.pro, function() {
					localStorageService.add('user_type', $scope.proUpdate.details);
					$scope.profile_user = localStorageService.get('user_id');
					window.location = "/";
					// $scope.responsePayment = paymentResource.update({id:$scope.profile_user},{id:$scope.profile_user,stripeToken:$scope.stripeToken}, function(){
					// 	localStorageService.remove('profesional');
					// 	window.location = "/";
					// });
				},function(error) {
					$scope.message = error.data;
				});
			};
			$scope.cancelSubmit = function(){
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();

				$scope.cancelMembership = cancelResource.save($scope.user, function() {
					localStorageService.add('user_type', $scope.cancelMembership.details);
					window.location = '/';
				},function(error) {
					$scope.message = error.data;
				});
			};



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
								zipcode: (!(types['postal_code'] === undefined || item.address_components[types['postal_code']] === undefined)?item.address_components[types['postal_code']]['short_name'] + ' ':''),
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
