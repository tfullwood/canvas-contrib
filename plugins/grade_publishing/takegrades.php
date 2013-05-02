<?php

switch ($_SERVER['REQUEST_METHOD'] ){
  case 'POST':
    // Read the php input and save it to a file.
    $fname = sprintf('takegrades_output/output_%s.txt',uniqid()); 
    print $fname;
    file_put_contents($fname,file_get_contents('php://input'));

    /*
     * Read the input sent via the script, parse it as CSV and save it in 
     * $grade_data_received which is an associative array
     */

    $grade_data_received = array();
    if (($handle = fopen($fname, "r")) !== FALSE) {
      $header_keys = array();
      $header_keys = fgetcsv($handle,0,",");
      while (($data = fgetcsv($handle, 0, ",")) !== FALSE) {
        $grade_data_received[] = array_combine($header_keys,array_pad($data,count($header_keys),"-"));
      }
    }
    // Do something else with the datea

    print_r($grade_data_received);
    break;
  case 'GET':
    print "Method not POST.  No good";
}
