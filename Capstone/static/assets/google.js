$(document).ready(function() {
    var map;
    var service;

    function initialise(location) {
        console.log("location:" + location);
        var currentLocation = new google.maps.LatLng(location.coords.latitude, location.coords.longitude);
        var mapOption = {
            center : currentLocation,
            zoom : 14,
            mapTypeId : google.maps.MapTypeId.ROADMAP,
        };

        map = new google.maps.Map(document.getElementById("map-canvas"), mapOption);
        var marker = new google.maps.Marker({
            position : currentLocation,
            map : map,
        });
        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');


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

            var content = '<p><a href="/menus/gid/'+place.place_id+'/'+place.name+'">See this menu</a></p>'

            var infowindow = new google.maps.InfoWindow({
                content:('<div><strong>' + place.name + '</strong><br>' +
                'Place ID: ' + place.place_id + '<br>' +
                place.formatted_address + content)
            });

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map, marker);
                var latitude = this.position.lat();
                var longitude = this.position.lng();
                console.log(this.position);
            });
        }
        google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
            var input = $("#search").val();
            var query = (input != '' )? input : "starbucks";
            performSearch(query);
        });
        function performSearch(q){
            var request ={
                bounds: map.getBounds(),
                query:String(q)
            };
            service.textSearch(request, callback);
        }
    }

    function initializer() {
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            zoom: 13,
        });

        if(navigator.geolocation) {
            browserSupportFlag = true;
            navigator.geolocation.getCurrentPosition(function(position) {
                initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                map.setCenter(initialLocation);
                var marker = new google.maps.Marker({
                    position : initialLocation,
                    map : map,
                });
                marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
            }, function() {
                handleNoGeolocation(browserSupportFlag);
            });
        }
         }

    google.maps.event.addDomListener(window, 'load', initializer);

    $(".getSearch").click(function () {
        navigator.geolocation.getCurrentPosition(initialise);
    });
});