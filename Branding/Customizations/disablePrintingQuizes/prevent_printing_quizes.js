/*
 * This script will make it so that students and observers cannot print quizzes.  It adds
 * a CSS document to the page that is only used when printing (media="print").  This CSS
 * file hides the body of the page, essentially hiding it from view when printing.  It is
 * not a foolproof solution but works as far as my limited testing shows.
 *
 * NOTE:  Please read and understand this script.  It comes with no guarantees.  Use at
 * your own risk.  Because it modifies the quiz pages, you will want to make sure it does
 * not interfere with the normal quiz-taking process.
 *
 */

// Edit this line to match the full path to where the noprint.css file is located at
var base_url_for_links = "https://s3.amazonaws.com/SSL_Assets/kevin/css/";

$(document).ready(function () {
  if(window.location.href.match(/quizzes\/\d+\/take/)){
      var course_id = ENV.context_asset_string.split('_')[1];
      var data2send = {'role':['StudentViewEnrollment','StudentEnrollment','ObserverEnrollment']};
      $.get('https://'+window.location.hostname+'/api/v1/users/'+ENV.current_user_id+'/enrollments',data2send,function(_data){
          for(ei=0;ei<_data.length;ei++){
            if(_data[ei].course_id == course_id){
              console.log(_data[ei]);
              $('head').append('<link rel="stylesheet" href="' + base_url_for_links + 'noprint.css" media="print" type="text/css" />');
            }
          }
        });
  }
});
