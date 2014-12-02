/*
 * README.
 * When a user is viewing an assignment submission, the file does not automatically
 * preview for images (maybe not other filetypes either).  This javascript makes uploaded
 * images render below the "File Uploads" box.
 *
 * Disclaimer: This script is distributed with no guarantee, warrantee, or any other type
 * of '-antee'.  No support is provided either.  You use at your own judgement and need to understand
 * that your are responsible for it working or not working.
 */

var pr = {
  init : function(){
    var pat = /courses\/[\d]*\/assignments\/[\d]*\/submissions\/[\d]*/;
    if(pat.test(window.location.href)){
        var iframe = window.frames[1];
        // console.log($(iframe).width());
        var content = $(iframe.document.getElementById('content'));
        var a = content.find('a.comment_attachment_link.image'); 
        var img = new Image();
        img.src = a.attr('href');

        var content_wrapper = iframe.document.getElementById('content-wrapper');
        $(img).insertAfter(content_wrapper);
        img.onload = function(){
          // console.log(img.width);
          if(img.width>$(iframe).width()){
            $(img).attr('width', '100%');
          }
        };
      }
  }
};


var b1;
$(document).ready(function(){
  
  for(x=0;x<$('b').length;x++){ 
    if($($('b')[x]).text()=='Assigned Peer Reviews'){ 
      b1=$('b')[x];
      break;
    }
  }

  if(b1!===undefined){
    var l = $(b1.nextElementSibling);
    var reviews = l.find('a:visible');
    // Count the reviews, save the list to a cookie for use later.
  }
  pr.init()
});


