
// A regex to recognize a string with numbers only
var ro = /^(\d+)$/;

/*
 * This function figures out the course id of the DOM element passed to it.
 *
 * @param li_obj a list item <item> identified by a previous jquery selector
 * @return the id or null
 *
 */
function getCourseId(li_obj){
  var _id = li_obj.id.replace('course_','');
  var res = ro.exec(_id);
  if(res){
    return res[1];
  }else{
    return null;
  }
}

// a template for the delete course link
var del_link = " | <a href='/courses/{{cid}}/confirm_action?event=delete'>Delete</a>";

// This is the function you would call to add the delete function to the page.  I wouldn't
// add this function to all courses, but call it using chrome's developer tools or firebug
// in Firefox.
function addCourseDeleteBtn(){
  var ll = $("li.course[id]");
  for(var l=0;l<ll.length; l++){
    var _id = getCourseId(ll[l]);
    if(_id !== null){
      var new_link = del_link.replace('{{cid}}',_id);

      var link_span = $("li.course[id=course_"+_id + "]>div.course>div.info>span.links");
      //console.log(link_span);
      //$(new_link).insertAfter(link_span.);
      $(link_span).append(new_link);
    }
  }
}

