/*
 * This is an unsupported, community-created project. Keep that in 
 * mind. Instructure won't be able to help you fix or debug this.
 * That said, the community will hopefully help support and keep
 * both the script and this documentation up-to-date.
 * 
 * Good luck!
 */
$(document).ready(function(){
 if(window.location.pathname.search('grades')>0){
    $('td.assignment_score').unbind();
    $.each($('td.assignment_score span.tooltip_wrap'),function(idx,val){
      if($(val).text().trim() == 'Click to test a different score'){
        $(val).hide();
        $(val).attr('title','');
        $(val).parents('td.assignment_score').attr('title','');
      }
      return null;
    });
    $('a.toggle_comments_link.tooltip').hide();
 }
});
