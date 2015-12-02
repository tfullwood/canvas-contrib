/*This is the carousel. Look for carousel-caption in this text and you will see where to change the text. do not change the layout or formatting as it will break*/
$('#home-page #feature').after(
	"<div class=\"hero-unit row\"> <!-- Carousel ================================================== --> <div id=\"highlight_carousel\" class=\"carousel slide\"> <div class=\"carousel-inner\">         <div class=\"item slide_one active\"> <div class=\"item-wrap\">  <div class=\"carousel-caption caption-left\"><h3 class=\"bannertext\"><span class=\"redsim slide_one_top\"> TOP TEXT </span><span class=\"whitesim slide_one_bottom\">BOTTOM TEXT</span></h3></div> </div> </div>         <div class=\"item slide_two\"> <div class=\"item-wrap\"> <div class=\"carousel-caption caption-right\"><h3 class=\"bannertext\"><span class=\"redsim slide_two_top\"> TOP TEXT SLIDE 2 </span><span class=\"whitesim slide_two_bottom\">BOTTOM TEXT SLIDE 2</span></h3></div> </div> </div>                       </div> <a class=\"left carousel-control\" href=\"#highlight_carousel\" data-slide=\"prev\" style=\"left: 35px;\"></a> <a class=\"right carousel-control\" href=\"#highlight_carousel\" data-slide=\"next\"></a> </div> <!-- /.carousel --> </div>"
);


//auto-refresh the carousel you dont need to touch this
$('#highlight_carousel').carousel({
	interval: 10000
});
$('.DashboardNavigation').before(
	"<div class='dashboardheading'><div class='dashcontainer'><span class='headingfordashboard'>Dashboard</span></div></div>"
);
$("#home-page #feature").hide();
$(".product-details #description h3").hide();
$(".product-details #description a").hide();
$(".product-details #description div a").show();
$('.hero-region.jumbotron.container .col-md-6:nth-child(1)').attr('class',
	'col-md-4 col-sm-6 col-xs-12 pull-right');
$('.hero-region.jumbotron.container .col-md-6:nth-child(2)').attr('class',
	'col-md-8 col-sm-6 col-xs-12 pull-left');

$(".product-details #description .container h3").show();

$(window).load(function() {
  $("#home-page").show();
});
