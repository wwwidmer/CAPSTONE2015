/**
 * Created by wwidmer on 6/9/15.
 */

$(document).ready(function() {
	$("#searchWarning").hide();
	$("#getSearch").click(function() {
		var search = $("#search").val();
		if (search.length < 1) {
			$("#searchWarning").show();
			$("#searchWarning.alert.alert-danger").html("Please enter a search term.");
		} else {
			window.open("/search/results?search=" + search);
		}
	});
});

$(document).ready(function() {
	// Ajax template
	$("form").click(function() {
		$.get("http://127.0.0.1:8000/ajax/review/fid", {
			fid : getID()
		}, function(data) {
			console.log(data);
		});
	});
	function getID() {
		return $("#fid").html();
	}

});

// Five star js
$(document).ready(function() {
	var radioB = $("input[name=rating]");
	var savedState = 0;
	$("#fiveStar li input#fiveStar_0").parent().remove();
	radioB.click(function() {
		numberOfStars = $("input[name=rating]:checked").val();
		savedState = numberOfStars;
		setStars(numberOfStars);
	});
	$("#fiveStar li").mouseover(function() {
		numberOfStars = $(this).children("label").children("input").attr("value");
		setStars(numberOfStars);
	});
	$("#fiveStar").mouseleave(function() {
		setStars(savedState);
	});
	function setStars(numberOfStars) {
		$("#fiveStar li:lt(" + 1 + numberOfStars + ")").css("background", "url('/static/assets/images/star.png') no-repeat");
		$("#fiveStar li:gt(" + numberOfStars + ")").css("background", "url('/static/assets/images/no-star.png') no-repeat");
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

		var img_url = "http://maps.googleapis.com/maps/api/staticmap?center=" + latlon + "&zoom=14&size=400x300&sensor=false";
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

function food() {
	$.get("http://127.0.0.1:8000/ajax/food/", {
		fid : getID()
	}, function(data) {
		console.log(data);
		var dd = JSON.parse(data);
		$(".name").html(dd[0].fields['name']);
		$(".logo img").attr('src', 'static/' + dd[0].fields['logo']);
	});
}

function menu() {
	$.get("http://127.0.0.1:8000/ajax/menu/", {
		mid : getID()
	}, function(data) {
		console.log(data);
		var dd = JSON.parse(data);
		$(".name").html(dd[0].fields['title']);
		$(".logo img").attr('src', 'static/' + dd[0].fields['logo']);
	});
}

function review() {
	$.get("http://127.0.0.1:8000/ajax/review/", {
		fid : getID()
	}, function(data) {
		console.log(data);
		var dd = JSON.parse(data);
		$(".name").html("");
		for (var i = 0; i < dd.length; i++) {
			$(".name").append(dd[i].fields['review'] + "</br>");
		}
	});
}

function getID() {
	return $("#get").val();
}

//Jssor Jquery Slider Show

jQuery(document).ready(function($) {
	//Reference http://www.jssor.com/development/slider-with-slideshow-jquery.html
	//Reference http://www.jssor.com/development/tool-slideshow-transition-viewer.html

	var _SlideshowTransitions = [
	//Fade Twins
	{
		$Duration : 700,
		$Opacity : 2,
		$Brother : {
			$Duration : 1000,
			$Opacity : 2
		}
	},
	//Rotate Overlap
	{
		$Duration : 1200,
		$Zoom : 11,
		$Rotate : -1,
		$Easing : {
			$Zoom : $JssorEasing$.$EaseInQuad,
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Round : {
			$Rotate : 0.5
		},
		$Brother : {
			$Duration : 1200,
			$Zoom : 1,
			$Rotate : 1,
			$Easing : $JssorEasing$.$EaseSwing,
			$Opacity : 2,
			$Round : {
				$Rotate : 0.5
			},
			$Shift : 90
		}
	},
	//Switch
	{
		$Duration : 1400,
		x : 0.25,
		$Zoom : 1.5,
		$Easing : {
			$Left : $JssorEasing$.$EaseInWave,
			$Zoom : $JssorEasing$.$EaseInSine
		},
		$Opacity : 2,
		$ZIndex : -10,
		$Brother : {
			$Duration : 1400,
			x : -0.25,
			$Zoom : 1.5,
			$Easing : {
				$Left : $JssorEasing$.$EaseInWave,
				$Zoom : $JssorEasing$.$EaseInSine
			},
			$Opacity : 2,
			$ZIndex : -10
		}
	},
	//Rotate Relay
	{
		$Duration : 1200,
		$Zoom : 11,
		$Rotate : 1,
		$Easing : {
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Round : {
			$Rotate : 1
		},
		$ZIndex : -10,
		$Brother : {
			$Duration : 1200,
			$Zoom : 11,
			$Rotate : -1,
			$Easing : {
				$Opacity : $JssorEasing$.$EaseLinear,
				$Rotate : $JssorEasing$.$EaseInQuad
			},
			$Opacity : 2,
			$Round : {
				$Rotate : 1
			},
			$ZIndex : -10,
			$Shift : 600
		}
	},
	//Doors
	{
		$Duration : 1500,
		x : 0.5,
		$Cols : 2,
		$ChessMode : {
			$Column : 3
		},
		$Easing : {
			$Left : $JssorEasing$.$EaseInOutCubic
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1500,
			$Opacity : 2
		}
	},
	//Rotate in+ out-
	{
		$Duration : 1500,
		x : -0.3,
		y : 0.5,
		$Zoom : 1,
		$Rotate : 0.1,
		$During : {
			$Left : [0.6, 0.4],
			$Top : [0.6, 0.4],
			$Rotate : [0.6, 0.4],
			$Zoom : [0.6, 0.4]
		},
		$Easing : {
			$Left : $JssorEasing$.$EaseInQuad,
			$Top : $JssorEasing$.$EaseInQuad,
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1000,
			$Zoom : 11,
			$Rotate : -0.5,
			$Easing : {
				$Opacity : $JssorEasing$.$EaseLinear,
				$Rotate : $JssorEasing$.$EaseInQuad
			},
			$Opacity : 2,
			$Shift : 200
		}
	},
	//Fly Twins
	{
		$Duration : 1500,
		x : 0.3,
		$During : {
			$Left : [0.6, 0.4]
		},
		$Easing : {
			$Left : $JssorEasing$.$EaseInQuad,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$Outside : true,
		$Brother : {
			$Duration : 1000,
			x : -0.3,
			$Easing : {
				$Left : $JssorEasing$.$EaseInQuad,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2
		}
	},
	//Rotate in- out+
	{
		$Duration : 1500,
		$Zoom : 11,
		$Rotate : 0.5,
		$During : {
			$Left : [0.4, 0.6],
			$Top : [0.4, 0.6],
			$Rotate : [0.4, 0.6],
			$Zoom : [0.4, 0.6]
		},
		$Easing : {
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1000,
			$Zoom : 1,
			$Rotate : -0.5,
			$Easing : {
				$Opacity : $JssorEasing$.$EaseLinear,
				$Rotate : $JssorEasing$.$EaseInQuad
			},
			$Opacity : 2,
			$Shift : 200
		}
	},
	//Rotate Axis up overlap
	{
		$Duration : 1200,
		x : 0.25,
		y : 0.5,
		$Rotate : -0.1,
		$Easing : {
			$Left : $JssorEasing$.$EaseInQuad,
			$Top : $JssorEasing$.$EaseInQuad,
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1200,
			x : -0.1,
			y : -0.7,
			$Rotate : 0.1,
			$Easing : {
				$Left : $JssorEasing$.$EaseInQuad,
				$Top : $JssorEasing$.$EaseInQuad,
				$Opacity : $JssorEasing$.$EaseLinear,
				$Rotate : $JssorEasing$.$EaseInQuad
			},
			$Opacity : 2
		}
	},
	//Chess Replace TB
	{
		$Duration : 1600,
		x : 1,
		$Rows : 2,
		$ChessMode : {
			$Row : 3
		},
		$Easing : {
			$Left : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1600,
			x : -1,
			$Rows : 2,
			$ChessMode : {
				$Row : 3
			},
			$Easing : {
				$Left : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2
		}
	},
	//Chess Replace LR
	{
		$Duration : 1600,
		y : -1,
		$Cols : 2,
		$ChessMode : {
			$Column : 12
		},
		$Easing : {
			$Top : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1600,
			y : 1,
			$Cols : 2,
			$ChessMode : {
				$Column : 12
			},
			$Easing : {
				$Top : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2
		}
	},
	//Shift TB
	{
		$Duration : 1200,
		y : 1,
		$Easing : {
			$Top : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1200,
			y : -1,
			$Easing : {
				$Top : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2
		}
	},
	//Shift LR
	{
		$Duration : 1200,
		x : 1,
		$Easing : {
			$Left : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1200,
			x : -1,
			$Easing : {
				$Left : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2
		}
	},
	//Return TB
	{
		$Duration : 1200,
		y : -1,
		$Easing : {
			$Top : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$ZIndex : -10,
		$Brother : {
			$Duration : 1200,
			y : -1,
			$Easing : {
				$Top : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2,
			$ZIndex : -10,
			$Shift : -100
		}
	},
	//Return LR
	{
		$Duration : 1200,
		x : 1,
		$Delay : 40,
		$Cols : 6,
		$Formation : $JssorSlideshowFormations$.$FormationStraight,
		$Easing : {
			$Left : $JssorEasing$.$EaseInOutQuart,
			$Opacity : $JssorEasing$.$EaseLinear
		},
		$Opacity : 2,
		$ZIndex : -10,
		$Brother : {
			$Duration : 1200,
			x : 1,
			$Delay : 40,
			$Cols : 6,
			$Formation : $JssorSlideshowFormations$.$FormationStraight,
			$Easing : {
				$Top : $JssorEasing$.$EaseInOutQuart,
				$Opacity : $JssorEasing$.$EaseLinear
			},
			$Opacity : 2,
			$ZIndex : -10,
			$Shift : -100
		}
	},
	//Rotate Axis down
	{
		$Duration : 1500,
		x : -0.1,
		y : -0.7,
		$Rotate : 0.1,
		$During : {
			$Left : [0.6, 0.4],
			$Top : [0.6, 0.4],
			$Rotate : [0.6, 0.4]
		},
		$Easing : {
			$Left : $JssorEasing$.$EaseInQuad,
			$Top : $JssorEasing$.$EaseInQuad,
			$Opacity : $JssorEasing$.$EaseLinear,
			$Rotate : $JssorEasing$.$EaseInQuad
		},
		$Opacity : 2,
		$Brother : {
			$Duration : 1000,
			x : 0.2,
			y : 0.5,
			$Rotate : -0.1,
			$Easing : {
				$Left : $JssorEasing$.$EaseInQuad,
				$Top : $JssorEasing$.$EaseInQuad,
				$Opacity : $JssorEasing$.$EaseLinear,
				$Rotate : $JssorEasing$.$EaseInQuad
			},
			$Opacity : 2
		}
	},
	//Extrude Replace
	{
		$Duration : 1600,
		x : -0.2,
		$Delay : 40,
		$Cols : 12,
		$During : {
			$Left : [0.4, 0.6]
		},
		$SlideOut : true,
		$Formation : $JssorSlideshowFormations$.$FormationStraight,
		$Assembly : 260,
		$Easing : {
			$Left : $JssorEasing$.$EaseInOutExpo,
			$Opacity : $JssorEasing$.$EaseInOutQuad
		},
		$Opacity : 2,
		$Outside : true,
		$Round : {
			$Top : 0.5
		},
		$Brother : {
			$Duration : 1000,
			x : 0.2,
			$Delay : 40,
			$Cols : 12,
			$Formation : $JssorSlideshowFormations$.$FormationStraight,
			$Assembly : 1028,
			$Easing : {
				$Left : $JssorEasing$.$EaseInOutExpo,
				$Opacity : $JssorEasing$.$EaseInOutQuad
			},
			$Opacity : 2,
			$Round : {
				$Top : 0.5
			}
		}
	}];

	var options = {
		$FillMode : 1, //[Optional] The way to fill image in slide, 0 stretch, 1 contain (keep aspect ratio and put all inside slide), 2 cover (keep aspect ratio and cover whole slide), 4 actual size, 5 contain for large image, actual size for small image, default value is 0
		$DragOrientation : 3, //[Optional] Orientation to drag slide, 0 no drag, 1 horizental, 2 vertical, 3 either, default value is 1 (Note that the $DragOrientation should be the same as $PlayOrientation when $DisplayPieces is greater than 1, or parking position is not 0)
		$AutoPlay : true, //[Optional] Whether to auto play, to enable slideshow, this option must be set to true, default value is false
		$AutoPlayInterval : 2500, //[Optional] Interval (in milliseconds) to go for next slide since the previous stopped if the slider is auto playing, default value is 3000
		$SlideshowOptions : {//[Optional] Options to specify and enable slideshow or not
			$Class : $JssorSlideshowRunner$, //[Required] Class to create instance of slideshow
			$Transitions : _SlideshowTransitions, //[Required] An array of slideshow transitions to play slideshow
			$TransitionsOrder : 1, //[Optional] The way to choose transition to play slide, 1 Sequence, 0 Random
			$ShowLink : true //[Optional] Whether to bring slide link on top of the slider when slideshow is running, default value is false
		},

		$BulletNavigatorOptions : {//[Optional] Options to specify and enable navigator or not
			$Class : $JssorBulletNavigator$, //[Required] Class to create navigator instance
			$ChanceToShow : 2, //[Required] 0 Never, 1 Mouse Over, 2 Always
			$AutoCenter : 1, //[Optional] Auto center navigator in parent container, 0 None, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
			$Steps : 1, //[Optional] Steps to go for each navigation request, default value is 1
			$Lanes : 1, //[Optional] Specify lanes to arrange items, default value is 1
			$SpacingX : 10, //[Optional] Horizontal space between each item in pixel, default value is 0
			$SpacingY : 10, //[Optional] Vertical space between each item in pixel, default value is 0
			$Orientation : 1 //[Optional] The orientation of the navigator, 1 horizontal, 2 vertical, default value is 1
		}
	};

	var jssor_slider1 = new $JssorSlider$("slider1_container", options);

	//responsive code begin
	//you can remove responsive code if you don't want the slider scales while window resizes
	function ScaleSlider() {
		var parentWidth = jssor_slider1.$Elmt.parentNode.clientWidth;
		if (parentWidth)
			jssor_slider1.$ScaleWidth(Math.min(parentWidth, 600));
		else
			window.setTimeout(ScaleSlider, 30);
	}

	ScaleSlider();

	$(window).bind("load", ScaleSlider);
	$(window).bind("resize", ScaleSlider);
	$(window).bind("orientationchange", ScaleSlider);
	//responsive code end
}); 