/*
 *
 * This file has a variety of usefull javascript functions.
 *
 */
function onPage(regex, fn) {
  if (location.pathname.match(regex)) fn();
}

function hasAnyRole(/*roles, cb*/) {
  var roles = [].slice.call(arguments, 0);
  var cb = roles.pop();
  for (var i = 0; i < arguments.length; i++) {
    if (ENV.current_user_roles.indexOf(arguments[i]) !== -1) {
      return cb(true);
    }
  }
  return cb(false);
}

function isUser(id, cb) {
  cb(ENV.current_user_id == id);
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

/*
 * Here are examples of the above scripts being used
 */
onPage(/\/courses\/\d+\/settings/, function() {
  // do something if on a course settings page
});

hasAnyRole('admin', function(hasRole) {
  if (hasRole) {
    // do something if the user is an admin anywhere
  } else {
    // otherwise do something else
  }
});

isUser(1, function(isRyan) {
  if (isRyan) {
    // do something if the canvas user id matches 1
  } else {
    // so something else
  }
});

onElementRendered('a[href=#create_ticket]', function(el) {
  // do something with el (a jquery element collection) once it is visible on the page
});

