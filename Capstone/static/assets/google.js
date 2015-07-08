var map;
var service;

function initialise(location) {
	console.log("location:" + location);
	var currentLocation = new google.maps.LatLng(location.coords.latitude, location.coords.longitude);

	var mapOption = {
		center : currentLocation,
		zoom : 11,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map-canvas"), mapOption);

	var marker = new google.maps.Marker({
		position : currentLocation,
		map : map
	});

	service = new google.maps.places.PlacesService(map);
	google.maps.event.addListenerOnce(map, 'bounds_changed', performSearch);

	function handleSearchResults(results, status) {
		console.log(results)
	}

	function callback(results, status) {
		if (status == google.maps.places.PlacesServiceStatus.OK) {
			for (var i = 0; i < results.length; i++) {
				createMarker(results[i]);
			}
		}
	}

	function createMarker(place) {
		var placeLoc = place.geometry.location;
		var marker = new google.maps.Marker({
			map : map,
			position : place.geometry.location
		});

		var content =
                   '<p><a href="http://www.starbucks.com/">See Review for this branch</a></p>'





                  var infowindow = new google.maps.InfoWindow({
                    content:('<div><strong>' + place.name + '</strong><br>' +
                                            'Place ID: ' + place.place_id + '<br>' +
                     place.vicinity + content)
                    });

		google.maps.event.addListener(marker, 'click', function() {
			infowindow.open(map, marker);
			var latitude = this.position.lat();
			var longitude = this.position.lng();
			console.log(this.position);
		});

	}

	function performSearch() {
		var request = {
			bounds : map.getBounds(),
			name : "starbucks"
		}
		service.nearbySearch(request, callback);
	}

}

navigator.geolocation.getCurrentPosition(initialise);

