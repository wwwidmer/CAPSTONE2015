/**
 * Created by wwidmer on 6/9/15.
 */

$(document).ready(function(){
    $("#getSearch").click(function(){
        var search = $("#search").val();
        window.open("search/results?search="+search);
    });
});


$(document).ready(function(){
    // Ajax template
    $("form").click(function(){
        $.get("http://127.0.0.1:8000/ajax/review/fid",{fid:getID()},function(data) {
          //  console.log(data);
        });
    });
    function getID(){
        return $("#fid").html();
    }
});

// Five star js
$(document).ready(function(){
    var radioB = $("input[name=rating]");
    var savedState = 0;
    $("#fiveStar li input#fiveStar_0").parent().remove();
    radioB.click(function(){
        numberOfStars = $("input[name=rating]:checked").val();
        savedState = numberOfStars;
        setStars(numberOfStars);
    });
    $("#fiveStar li").mouseover(function(){
        numberOfStars = $(this).children("label").children("input").attr("value");
        setStars(numberOfStars);
    });
    $("#fiveStar").mouseleave(function(){
        setStars(savedState);
    });
    function setStars(numberOfStars){
        $("#fiveStar li:lt("+1+numberOfStars+")").css("background","url('/static/assets/images/star.png') no-repeat");
        $("#fiveStar li:gt("+numberOfStars+")").css("background","url('/static/assets/images/no-star.png') no-repeat");
    }
});

// Google maps demo
$(document).ready(function() {
    var x = document.getElementById("demo");

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            x.innerHTML = "Geolocation is not supported by this browser.";
        }
    }

    function showPosition(position) {
        var latlon = position.coords.latitude + "," + position.coords.longitude;

        var img_url = "http://maps.googleapis.com/maps/api/staticmap?center="
            + latlon + "&zoom=14&size=400x300&sensor=false";
        document.getElementById("mapholder").innerHTML = "<img src='" + img_url + "'>";
    }

    function showError(error) {
        switch (error.code) {
            case error.PERMISSION_DENIED:
                x.innerHTML = "User denied the request for Geolocation.";
                break;
            case error.POSITION_UNAVAILABLE:
                x.innerHTML = "Location information is unavailable.";
                break;
            case error.TIMEOUT:
                x.innerHTML = "The request to get user location timed out.";
                break;
            case error.UNKNOWN_ERROR:
                x.innerHTML = "An unknown error occurred.";
                break;
        }
    }
});

