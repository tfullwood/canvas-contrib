/*
	Add "Show More Imports" Button on SIS Imports Page
	By: Mike Cotterman, Marion Technical College
	Disclaimer: This script is offered as-is without any warranty, so if you decide to use it you take on all the risk.
				 Also, the script may stop operating or not operate as expected if changes are made to the Canvas UI.
*/
$.ajaxSetup({
  dataFilter: function(data, type) {
    var prefixes = ['//', 'while(1);', 'while(true);', 'for(;;);'],
      i, l, pos;
    if (type != 'json' && type != 'jsonp') {
      return data;
    }
    for (i = 0, l = prefixes.length; i < l; i++) {
      pos = data.indexOf(prefixes[i]);
      if (pos === 0) {
        return data.substring(prefixes[i].length);
      }
    }
    return data;
  }
});

var templates={},
    get_templates_called=false,
    get_templates = function(callback){
      chrome.runtime.sendMessage({req: "get_templates"}, function(response) {
        //console.log(response.farewell);
        //console.log('response',response);
        //console.log(response.templates);
        //alert(response);
        $(response.templates).each(function(idx,t){
          //console.log('idx',idx);
          //console.log('t',t);
          templates[t.name] = Handlebars.compile(t.source);

        });
        get_templates_called = true;
        callback(templates);
      });
      
    },
    get_template = function(name){
      return templates[name];
    };

var see_messages = function(e){
  //console.log('data-id',$(this).data('id'));
  e.preventDefault();
  $('#'+$(this).data('id')).toggle();
};

var parseQueryString = function( queryString ) {
    var params = {}, queries, temp, i, l;
 
    // Split into key/value pairs
    //console.log('queryString',queryString);
    queries = queryString.split("&");
 
    // Convert the array of strings into an object
    for ( i = 0, l = queries.length; i < l; i++ ) {
        temp = queries[i].split('=');
        params[temp[0]] = temp[1];
    }
 
    return params;
};
var parse_canvas_link_headers = function(link_header_string){
  var links = {};

  //var parts = link_header_string.split(',');
  $(link_header_string.split(',')).each(function(idx,part){
    var part_split = part.split(';');
    var url = part_split[0].replace('<','').replace('>','');
    var key = part_split[1].split('=')[1].replace(/"/g,'');
    links[key] = {url:url,params:parseQueryString(url)};
  });

  //console.log('links',links);
  return links;
};


var init_loaded = false,
    user_details_dialog;

var row_data_loaded = function(data, status, xhr){
  var callbacks = {}
  var links = parse_canvas_link_headers(xhr.getResponseHeader('link'));
  if(links == null || !links.next ){
    $('a#more_sis_load_more').remove();
  }else{
    //console.log('parsed',links.current.params);
    current_page_number = links.current.params.page;
  }
  $('a#show_more_sis').remove();

  if(!init_loaded){
    /*
    var table_data = get_template('more_sis_container')({
      trows:get_template('get_more_data_row')({
        trows:more_sis_table_data(data,callbacks)
      })
    });
    */
    var trows;
    dust.render('get_more_data_row.html',{
        trows:more_sis_table_data(data,callbacks)
      },function(erro,out){
        trows = out;    
    });
    dust.render('more_sis_container.html',{
      trows:trows
    },function(err,out){
      $('div.last_batch').after(out);
      setup_scroll_listening();
    });

    $('#cant_record_dialog').after("<div id='sis_user_dialog'></div>");
    user_details_dialog = $("#sis_user_dialog").dialog({
				autoOpen: false,
				modal: true,
				width: 600,
				height: 300,
        appendTo:'#more_sis_container',
				buttons: {
					"Dismiss": function() {
						$(this).dialog("close");
					}
				}
			});
    init_loaded = true;
  }else{

    /*
    var table_data = get_template('get_more_data_row')({
        trows:more_sis_table_data(data,callbacks)
    });
    */
    dust.render('get_more_data_row.html',{
        trows:more_sis_table_data(data,callbacks)
    },function(err,out){
      $('table#more_sis_table tbody').append(out);
    });


    $('div#more_sis_container').data('page',current_page_number);

    loading = false;
    $('.loading_animation_image').hide(); //hide loading image once data is received
                
    $('.sis_imports_see_messages')
       .off('click.sis_import_see_messages')
        .on('click.sis_import_see_messages',see_messages);
    ////
  }



  console.log('callbacks',callbacks);
  var vals = Object.keys(callbacks).map(function (key) {
      return callbacks[key];
  });
  $(vals).each(function(idx,cb){
    console.log('idx',idx,'cb',cb);
    if(typeof(cb.callback)==='function'){
      cb.callback();
    }
  });
  //console.log('.sis_imports_see_messages',$('.sis_imports_see_messages'));
};

var enhancementPatterns = [
  {
    label: 'login id already claimed',
    match_pattern : /^user ([\d\.-\w:@]*) has/i,
    action:function(message,matches){
      console.log('in action',matches);
      return message.replace(matches[1],"<a href='#' data-userid='"+matches[1]+"' class='element_toggler load_user_info'>"+matches[1]+"</a>");
    },
    callback:function(){
      console.log('in callback');
      $('.load_user_info')
        .off('click.load_user_info')
        .on('click.load_user_info',function(a){
          a.preventDefault();
          var t = $(this);
          console.log('user_info clicked',this);
          $.getJSON(
            '/api/v1/users/sis_user_id:'+t.data('userid')+'/profile',
            function(_d){ 
              //var user_details = get_template('user_details')(_d);
              dust.render('user_details.html',_d,function(err,out){
                user_details_dialog.dialog("option", "title", _d.name).dialog('open');
                console.log('got user information',_d,out);
                user_details_dialog.html(out);
              });
            })
            .fail(function(fail_message){
              console.log('failed to get user',fail_message)
              ;
            });
        });
    }
  }
];
var enhanceMessage = function(message,callbacks){
  // TODO find common phrases and  do usefull stuff before returning the message
  //
  
  $(enhancementPatterns).each(function(idx,pat){
    var matches=message.match(pat.match_pattern);
    if(matches){
      message = pat.action(message,matches);
      //console.log('pat.callback',pat.callback);
      callbacks[pat.label] = {label:pat.label,callback:pat.callback};
    }else{
      //console.log('no matches');
    }

  });

  return message
};

var encodeHtml = function(input,callbacks){
      input = input.replace(/>/g,'&gt;');
      input = input.replace(/</g,'&lt;');
      input = input.replace(/&/g,'&amp;');
      input = input.replace(/"/g,'&quot;');
      input = input.replace(/'/g,'&#39;');
      return enhanceMessage(input,callbacks);
    },

    more_sis_table_data = function(data,callbacks){
      var ret_data = [];
      data.sis_imports.forEach(function(val){
        var ret_row = val;
        ret_row.created = new Date(val.created_at).toLocaleString();
        if(typeof(val.ended_at) == 'string'){
          ret_row.finished = new Date(val.ended_at).toLocaleString();
        }else{
          ret_row.finished = '';
        }
        if(typeof(workflow_states[val.workflow_state]) == 'string') { 
          ret_row.workflow_state = workflow_states[val.workflow_state];
        }
        ret_row.has_messages = false;
        ret_row.errors = [];
        ret_row.warnings = [];
        if(typeof(val.processing_warnings) == 'object' || typeof(val.processing_errors) == 'object'){
          ret_row.has_messages = true;
          if(typeof(val.processing_warnings) == 'object'){
            val.processing_warnings.forEach(function(ws){
              //console.log(ws);

              ret_row.warnings.push( {
                filename : ws[0],
                message : encodeHtml(ws[1],callbacks)
              });
            });
          }
          if(typeof(val.processing_errors) == 'object'){
            ret_row.has_errors = true;

            val.processing_errors.forEach(function(ws){
              //console.log(ws);
              workflow_state = 'Error';

              ret_row.errors.push( {
                filename : ws[0],
                message : encodeHtml(ws[1],callbacks)
              });
            });
          }
        }
        if(typeof(val.data.counts) == 'object'){
          var counts_tmp = [];
          count_types.forEach(function(ctype){
            if(val.data.counts[ctype] > 0){
              counts_tmp.push({ctype:ctype,value:val.data.counts[ctype]});
            }
          });
          ret_row.data.counts = counts_tmp;
        }
        ret_data.push(ret_row);
      });
      //console.log('ret_data',ret_data);
      return ret_data;
   },
   load_data = function(page){
     if(!page){
       page=1;
     }
     var dummy = new Date().getTime();
     $.getJSON('/accounts/self/sis_imports?page='+page+'&dummy='+dummy, row_data_loaded).fail(function(_d,_m) {
          //console.log(_d,_m);
          $('a#show_more_sis')
            .text('Error loading results!')
            .toggleClass('btn-inverse',false)
            .toggleClass('btn-danger',true)
            .attr('id','show_more_sis');
     });
   },
   show_more_sis = function(e){
      e.preventDefault();
      var button = $(this);
      if(button.text().match(/Loading/i)) { return false; }
      button.text('Loading... Please wait...').toggleClass('btn-inverse', false);

      /*
      console.log('fetching templates');
      var start = new Date();
      get_templates(function(_t){
        var end = new Date(),
            delta = end-start,
            minutes = Math.floor(delta / 60000),
            seconds = Math.floor((delta % 60000)/1000),
            milliseconds = (delta % 60000)%1000;
        console.log('done fetching templates',minutes+':'+seconds+':'+milliseconds);
          
        load_data();
      });
      */
      load_data();

    }, 
    more_data = true,
    loading = false,
    setup_scroll_listening = function(){
    
    $(window).scroll(function() { //detect page scroll
        
        if($(window).scrollTop() + $(window).height() == $(document).height())  //user scrolled to bottom of the page?
        {
            if(more_data && loading==false) //there's more data to load
            {
              $('.loading_animation_image').show(); //hide loading image once data is received
              loading = true;

              var load_page = parseInt($('div#more_sis_container').data('page'))+1;
              //if(load_page < 2) { load_page = 2; }
              load_data(load_page);
            }
        }
    });

  },
  count_types = new Array('abstract_courses','accounts','courses','enrollments','grade_publishing_results','group_memberships','groups','sections','terms','users','xlists'),
  workflow_states = {created: 'Created', importing: 'Importing', imported: 'Successfully Imported', imported_with_messages: 'Warning', failed_with_messages: 'Error', failed: 'Failed'};

$(document).ready(function(e) {
  if(location.href.search(/\/accounts\/\d+\/sis_import(\/#)?$/)>0){
    // Fetch compiled templates then start the ball rolling
    $('div.last_batch').after('<a id="show_more_sis" class="btn btn-inverse">SIS Imports History</a>');
    $('a#show_more_sis').click(show_more_sis);
  }
});
