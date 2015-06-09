/**
 * Created by wwidmer on 6/9/15.
 */

console.log("LOGGGG");

$(document).ready(function(){
    $("#getSearch").click(function(){
        var search = $("#search").val();
        window.open("search/results?search="+search);
    });
});

