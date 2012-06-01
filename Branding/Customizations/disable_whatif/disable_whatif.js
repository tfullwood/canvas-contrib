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

 }
});
