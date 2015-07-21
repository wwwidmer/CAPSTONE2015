/*
 FancyBox - image enlarge
 */
$(document).ready(function() {
	$(".fancybox").fancybox();

	/* item simple */
	$("#single_1").fancybox({
		helpers : {
			title : {
				type : 'float'
			}
		}
	});
	
	/* item review*/
	$(".fancybox-thumb").fancybox({
		prevEffect : 'none',
		nextEffect : 'none',
		helpers : {
			title : {
				type : 'outside'
			},
			thumbs : {
				width : 50,
				height : 50
			}
		}
	});
});

