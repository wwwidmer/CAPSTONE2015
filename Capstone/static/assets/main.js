/**
 * Created by wwidmer on 6/9/15.
 */

$(document).ready(function(){
    $("#searchWarning").hide();

   $(".getSearch").click(function(){
        var searchv = $("#search").val();
        if(searchv.length < 1) {
            $("#searchWarning").show();
            $("#searchWarning.alert.alert-danger").html("Please enter a search term.");
        } else {

            $.get("http://127.0.0.1:8000/ajax/search/", {search:searchv}, function (data) {
                console.log("data: " + data);
                var dd = JSON.stringify(data);

            });
        }
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




