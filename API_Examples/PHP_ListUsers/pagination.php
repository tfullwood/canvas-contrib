<?php
/**
 * This script will fetch the current final grades for all students in a specific course. 
 * In order for this to work, you need to be either a teacher in the course or an account 
 * admin.  Please take a moment to customize the variables in the top part of this script 
 * to fit your situation.  Specifically, adjust BASE_URL, ACCESS_TOKEN, and $course_id.
 *
 **/

// Variables you should adjust
$sub_domain = 'cwt'; # Set this to your account's sub-domain or url.  This is the 
                     # url you use to access canvas.  

define('BASE_URL',"https://$sub_domain.instructure.com/api/v1%s");  # Don't change this.
                     # The %s part is used to plug in the endpoints 
                     # later in the script.

define('ACCESS_TOKEN', "BhkYqp2zSxQ4wbSgEbZeBr3iO5KcRhJpcjTUaXGfs5dQ"); # Replace this with your user's access token

function fetchEnrollments($course_id=False){
  if(!$course_id){
    return array();
  }

  # Build the API endpoint for fetching the list of students
  $enrollment_params = array("page=1",'per_page=50');
  $enrollment_params_string = implode('&',$enrollment_params);

  $enrollments_endpoint = sprintf(BASE_URL,sprintf('/courses/%d/enrollments?%s', $course_id,$enrollment_params_string));

  # Initiate cURL, adding the REQUEST_HEADERS to it for authentication
  $ch = curlhandler($enrollments_endpoint,true);

  # Execute the request
  # Fetch the response, 
  $enrollment_list = curl_exec($ch);

  if(!$enrollment_list){
    print 'error fetching student list';
  }else{
    # Strip extra whitespace from the beginning and end then parse response into JSON
    list($header_string, $enrollment_list) = explode("\r\n\r\n", $enrollment_list, 2);
    
    $enrollment_list = trim($enrollment_list);
    $enrollment_list_2 = json_decode($enrollment_list,true);
    #print_r($enrollment_list_2);
  }

  $headers = parseHeaders($header_string);
  $links = parseLinks($headers['Link']);
  if($links==false){
    $enrollment_results = $enrollment_list_2;
  }else{
    //print_r($links);
    $curl_handlers = array();
    $mh = curl_multi_init();
    for($x=0;$x<(int)$links['num_pages'];$x++){
      # Initiate cURL, adding the REQUEST_HEADERS to it for authentication
      $enrollment_params = array("page=$x",'per_page='.$links['per_page']);
      $enrollment_params_string = implode('&',$enrollment_params);
      // Set url
      $rep_enrollments_endpoint = sprintf(BASE_URL,sprintf('/courses/%d/enrollments?%s', $course_id,$enrollment_params_string));
      $curl_handlers[$x] = curlHandler($rep_enrollments_endpoint);
      curl_multi_add_handle($mh,$curl_handlers[$x]); 
    }
    do{
          $mrc = curl_multi_exec($mh, $active);
    }while ($mrc == CURLM_CALL_MULTI_PERFORM);

    while($active && $mrc == CURLM_OK){
      if (curl_multi_select($mh) != -1) {
        do {
          $mrc = curl_multi_exec($mh, $active);
        } while ($mrc == CURLM_CALL_MULTI_PERFORM);
      }
    }
    
    $enrollment_results = array();
    for($i=0;$i<(int)$links['num_pages'];$i++){
      $content = curl_multi_getcontent($curl_handlers[$i]);
      $json_response = json_decode($content,true);

      if($json_response){
        $enrollment_results = array_merge($enrollment_results,$json_response);
      }
      curl_multi_remove_handle($mh,$curl_handlers[$i]);
    }
    curl_multi_close($mh);
  }
  return $enrollment_results;
}

function curlHandler($endpoint,$get_headers=False){
  $request_headers = array('Authorization: Bearer ' . ACCESS_TOKEN);
  # Initiate cURL, adding the REQUEST_HEADERS to it for authentication
  $ch = curl_init();

  // Set headers
  curl_setopt($ch,CURLOPT_HTTPHEADER,$request_headers);
  if($get_headers){
    curl_setopt($ch, CURLOPT_HEADER,true);
  }

  // Set url
  curl_setopt($ch, CURLOPT_URL,$endpoint);
  // Tell cURL to return the results of the request. 
  curl_setopt($ch,CURLOPT_RETURNTRANSFER,True);
  //
  return $ch;
}

function parseHeaders($header_string){
  $rows = explode("\r\n",$header_string);
  $headers = array();
  foreach($rows as $row=>$val){
    list($name,$value) = explode(':',$val,2);
    $headers[$name] = $value;
  }

  return $headers;
}
function parseLinks($LinkHeader){
  $link_headers = explode(",",$LinkHeader);
  if(!$link_headers){
    $tmp_obj = false; 
  }else{
    $links = array();
    #responseObject.getheaders('Links')
    #print responseObject.info()
    $per_page_pat = "/.*per_page=(?P<per_page>\d+)/";
    $page_pat = "/[^_]*page=(?P<page>\d+)/";

    $tmp_obj = array(
        'last'=>null,
        'next'=>null,
        'first'=>null,
        'count_estimate'=>null,
        'page'=>null,
        'per_page'=>null,
        'num_pages'=>null);
    foreach($link_headers as $link){
      $links[] = explode(';',$link);
    }
    foreach($links as $litem){
      $pp = array();
      preg_match_all($per_page_pat,$litem[0],$pp);
      $tmp_obj['per_page'] = $pp[1][0];
      $pn = array();
      preg_match($page_pat,$litem[0],$pn);
      if($litem[1]==' rel="next"'){
        $tmp_obj['page'] = $tmp_obj['per_page'] - 1;
        $tmp_obj['next'] = $tmp_obj['per_page'];
      }elseif($litem[1]==' rel="first"'){
        $tmp_obj['first'] = $tmp_obj['per_page'];
      }elseif($litem[1]==' rel="last"'){
        $tmp_obj['last'] = $tmp_obj['per_page'];
        # also do the count_estimate. i.e. per_page * page
        $ce = array();
        preg_match_all($page_pat,$litem[0],$ce);
        $tmp_obj['num_pages'] = $ce[1][0];
        $tmp_obj['count_estimate'] = $tmp_obj['per_page'] * $tmp_obj['num_pages'];
      }
    }
    #print tmp_obj
  }
  return $tmp_obj;
}

