if(window.location.href.indexOf('sis_import')>-1){
  var base_url = 'https://dl.dropboxusercontent.com/u/1647772/sis_loader_require_version/';
  require([base_url + 'dust-core.min.js', base_url + 'templates.js', base_url + 'sis_import_extras.js']);
}
