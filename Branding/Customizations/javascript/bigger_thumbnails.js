var img_list = $('img.media_comment_thumbnail');
for(var x=0;x<img_list.length;x++){
  var url = $(img_list[x]).css('background-image');
  if(url.indexOf('instructuremedia')>=0){
    /*
      //width/140/height/100/bgcolor/000000/type/2/vid_sec/5);
    */
    $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('width/140','width/480').replace('height/100','height/360'));
    //console.log($(img_list[x]).css('background-image'
  }else{
    // Works for youtube
    $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('2.jpg','0.jpg'));
  }
  $(img_list[x]).width('480px').height('360px')
}

