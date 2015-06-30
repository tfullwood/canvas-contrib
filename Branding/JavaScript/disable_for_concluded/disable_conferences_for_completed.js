
function onPage(regex, fn) {
  if (location.pathname.match(regex)) fn();
}
function onElementRendered(selector, cb, _attempts) {
  var el = $(selector);
  _attempts = ++_attempts || 1;
  if (el.length) return cb(el);
  if (_attempts == 60) return;
  setTimeout(function() {
    onElementRendered(selector, cb, _attempts);
  }, 250);
}

$(document).ready(function(){
  $('div.ig-admin a.join-button').hide();
  onPage(/\/conferences/,function(){
    onElementRendered('#new-conference-list',function(){
      var course_id = ENV.context_asset_string.split('_')[1];
      var url= '/api/v1/courses/'+course_id+'/enrollments?user_id=self';

      $.get(url).done(function (response) {
        if(response.length > 0 ){
          // Hide all of the conference join links
          $('div.ig-admin a.join-button').show();
        }else{
          $('div.ig-admin a.join-button').remove();

        }
      });
    });
  });
});
