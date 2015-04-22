////////////////////////
//Replace Favicon Code//
////////////////////////

$(document).ready(function() {
   var inputs = document.getElementsByTagName('link');
   	for(var i=0; i<inputs.length; i++){
    	if(inputs[i].type == "image/x-icon"){
    var old_link = inputs[i];
   var link = document.createElement('link');
   	link.type = 'image/x-icon';
   	link.rel = 'shortcut icon';
   	link.href = '';
   document.getElementsByTagName('head')[0].replaceChild(link, old_link);
    	}
	}
});