
function getCourseList1(){
  var ll = $("div.course>div.info>span.links>a:contains('Settings')");

  var cid_list = new Array();

  var ro = /\/courses\/(\d*)\/settings/;

  for(var x=0;x<ll.length; x++){
    var l1 = ll[x];
    var res = ro.exec(l1.attributes.href.value);
    console.log(res);
    if(res!==null){
      cid_list.push(res[1]);
    }
  }
}

var ro = /^(\d+)$/;
function getCourseList(){
  var ll = $("li.course[id]");
  var cid_list = new Array();
  for(var x=0;x<ll.length; x++){
    var _id = ll[x].id.replace('course_','');
    var res = ro.exec(_id);
    /*
    console.log(ll[x].id);
    console.log(res);
    */
    if(res){
      cid_list.push(res[1]);
    }
  }

  return cid_list;
}
var del_link = " | <a href='/courses/{{cid}}/confirm_action?event=delete'>Delete</a>";
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

function getCourseId(li_obj){
  var _id = li_obj.id.replace('course_','');
  var res = ro.exec(_id);
  if(res){
    return res[1];
  }else{
    return null;
  }
}
