/**
 * Created by wwidmer on 6/9/15.
 */

$(document).ready(function(){
    $("#searchWarning").hide();

    $("#search-low").click(function(){
       var search = $("#search").val();
        $.get("/ajax/search/", {"search":search}, function (data) {
            console.log(data);
            var dd = JSON.parse(data);
            $(".controls .menu, .controls .food").html("");
            $(".controls .menu, .controls .food").empty();
            $(".controls .menu").append("<h3> Menus </h3>");
            $(".controls .food").append("<h3> Food </h3>");
            for(var i = 0; i < dd.length;i++){
                if(dd[i].model == 'menu.menu') {
                    var menuColumn = "<div class='col-md-3'><a href='/menus/"+dd[i].pk +"'>" + dd[i].fields['menuName'] + "</a></div>";
                    $(".controls > .menu").append(menuColumn);
                } else
                {
                    var foodColumn = "<div class='col-md-3'><a href='/menus/food/"+dd[i].pk +"'>" + dd[i].fields['dishName'] + "</a></div>";
                    $(".controls > .food").append(foodColumn);
                }
            }
         });

    });
    $(".getSearch-menu").click(function(){
        var search = $("#search-menu").val();
        if(search.length < 1) {
            $("#searchWarning").show();
            $("#searchWarning.alert.alert-danger").html("Please enter a search term.");
        } else {
            window.open("/search/results?search=" + search);
        }
    });
});

function showonlyone(choice) {
    var toggle = document.getElementsByTagName("div");
    for(var x=0; x<toggle.length; x++) {
        name = toggle[x].getAttribute("class");
        if (name == 'toggle') {
            if (toggle[x].id == choice) {
                toggle[x].style.display = 'block';
            }
            else {
                toggle[x].style.display = 'none';
            }
        }
    }
}


/*
$(document).ready(function(){
    // Ajax template
    $("form").click(function(){
        $.get("http://127.0.0.1:8000/ajax/review/fid",{fid:getID()},function(data) {
          console.log(data);
        });
    });
    function getID(){
        return $("#fid").html();
    }
});
*/
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
/*
 function food(){
     $.get("http://127.0.0.1:8000/ajax/food/", {fid: getID()}, function (data) {
         console.log(data);
         var dd = JSON.parse(data);
         $(".name").html(dd[0].fields['name']);
         $(".logo img").attr('src','static/'+dd[0].fields['logo']);
     });
 }
 function menu(){
     $.get("http://127.0.0.1:8000/ajax/menu/", {mid: getID()}, function (data) {
         console.log(data);
         var dd = JSON.parse(data);
         $(".name").html(dd[0].fields['title']);
         $(".logo img").attr('src','static/'+dd[0].fields['logo']);
         });
 }
 function review(){
            $.get("http://127.0.0.1:8000/ajax/review/", {fid: getID()}, function (data) {
                console.log(data);
                var dd = JSON.parse(data);
                $(".name").html("");
                for(var i = 0; i < dd.length;i++){
                    $(".name").append(dd[i].fields['review'] + "</br>");
                }
            });
 }
 */
function getID() {
    return $("#get").val();
}

