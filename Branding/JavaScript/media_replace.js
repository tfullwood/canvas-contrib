/*
Support
======

This is an unsupported, community-created project. Keep that in 
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.

Good luck!
 * 
 */

/*
 * Create a link in a quiz question pointing to a link like this:
 *    https://personalleadership.instructure.com/courses/9/quizzes/6/take?preview=1
 *
 */

var PLE_DO_DEBUG = false; // Set to true if you want to see debugging in the console.
var _dbg = function(obj){
  if (PLE_DO_DEBUG === true){
    console.log(obj);
  }
}


$(document).ready(function(){
  /*
   * Do this only when viewing a quiz
   * https://personalleadership.instructure.com/courses/9/quizzes/6/take?preview=1
   */
  if(window.location.pathname.search('/quizzes/') && window.location.pathname.search('/take')){
    //var ipl_template_html = '<object id="kaltura_player_1345216546_{{obj_id}}" name="kaltura_player_1345216546_{{obj_id}}" type="application/x-shockwave-flash" allowFullScreen="true" allowNetworking="all" allowScriptAccess="always" height="360" width="400" bgcolor="#000000" xmlns:dc="http://purl.org/dc/terms/" xmlns:media="http://search.yahoo.com/searchmonkey/media/" rel="media:video" resource="https://www.kaltura.com/index.php/kwidget/cache_st/1345216546/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}" data="https://www.kaltura.com/index.php/kwidget/cache_st/1345216546/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}"><param name="allowFullScreen" value="true" /><param name="allowNetworking" value="all" /><param name="allowScriptAccess" value="always" /><param name="bgcolor" value="#000000" /><param name="flashVars" value="&" /><param name="movie" value="https://www.kaltura.com/index.php/kwidget/cache_st/1345216546/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}" /><a href="http://corp.kaltura.com/products/video-platform-features">Video Platform</a> <a href="http://corp.kaltura.com/Products/Features/Video-Management">Video Management</a> <a href="http://corp.kaltura.com/Video-Solutions">Video Solutions</a> <a href="http://corp.kaltura.com/Products/Features/Video-Player">Video Player</a> <a rel="media:thumbnail" href="https://cdnbakmi.kaltura.com/p/{{partner_id}}/sp/{{partner_id}}00/thumbnail/entry_id/{{entry_id}}/width/120/height/90/bgcolor/000000/type/2"></a> <span property="dc:description" content=""></span><span property="media:title" content="{{description}}"></span> <span property="media:width" content="400"></span><span property="media:height" content="360"></span> <span property="media:type" content="application/x-shockwave-flash"></span> </object>';
    /*
     * Edit this line.  It is essentially the entire embed code on one line.  Make sure
     * you replace all the important parts with {{obj_id}}, {{partner_id}} and
     * {{entry_id}}
     */
    var ipl_template_html = '<object id="kaltura_player_{{obj_id}}" name="kaltura_player" type="application/x-shockwave-flash" allowfullscreen="true" allownetworking="all" allowscriptaccess="always" height="360" width="400" xmlns:dc="http://purl.org/dc/terms/" xmlns:media="http://search.yahoo.com/searchmonkey/media/" rel="media:video" resource="https://www.kaltura.com/index.php/kwidget/cache_st/1345248391/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}" data="https://www.kaltura.com/index.php/kwidget/cache_st/1345248391/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}"><param name="allowFullScreen" value="true"> <param name="allowNetworking" value="all"> <param name="allowScriptAccess" value="always"> <param name="bgcolor" value="#000000"> <param name="flashVars" value=""> <param name="movie" value="https://www.kaltura.com/index.php/kwidget/cache_st/1345248391/wid/_{{partner_id}}/uiconf_id/{{uiconf_id}}/entry_id/{{entry_id}}"> <span property="dc:description" content=""></span> <span property="media:title" content="Kaltura Video"></span> <span property="media:width" content="400"></span> <span property="media:height" content="360"></span> <span property="media:type" content="application/x-shockwave-flash"></span> </object>'


    // Get all the media holders
    var ahrefs = $('#content a');
    for(var x=0; x < ahrefs.length; x++){
      // Get Unique information stored in the link
      var partner_id_pat = /partner_id\/(\d+)/g;
      var uiconf_id_pat = /uiconf_id\/\d+/g;
      var entry_id_pat = /entry_id\/\d+_\w+/g;


      var partner_id = ahrefs[x].href.match(partner_id_pat)
      var uiconf_id = ahrefs[x].href.match(uiconf_id_pat);
      var entry_id = ahrefs[x].href.match(entry_id_pat);

      if(entry_id == null || uiconf_id == null || partner_id === null){
        _dbg('kaltura link not found here');
      }else{
        _dbg('kaltura link found');
        //_dbg(ahrefs[x].href);
        partner_id = partner_id[0].split('/')[1];
        _dbg(partner_id); 
        _dbg(uiconf_id); 
        _dbg(entry_id); 
        uiconf_id = uiconf_id[0].split('/')[1];
        entry_id = entry_id[0].split('/')[1];

        _dbg(ahrefs[x]);
        // Fill the div with the html_template where {{media_id}} is replaced with the
        // media_id we pulled from the div
        ipl_template_html = ipl_template_html.replace(/{{partner_id}}/g,partner_id);
        ipl_template_html = ipl_template_html.replace(/{{entry_id}}/g,entry_id);
        ipl_template_html = ipl_template_html.replace(/{{uiconf_id}}/g,uiconf_id);
        ipl_template_html = ipl_template_html.replace(/{{description}}/g,ahrefs[x].textContent);
        ipl_template_html = ipl_template_html.replace(/{{obj_id}}/g,x);
        $(ahrefs[x]).replaceWith(ipl_template_html);
      }
    }
  }
});
