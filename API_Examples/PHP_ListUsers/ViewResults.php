<!DOCTYPE html>
<?php
require_once('pagination.php'); 
$enrollment_results = fetchEnrollments(279121);
?>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; class=MsoNormal>        <title></title>
<link rel="stylesheet" type="text/css" href="viewerCss.css" />
 
    </head>
    <body>
        <div id="menu">
            <ul>
                <li><a href="index.php">Home</a></li>
                <li><a href="ViewEnrollments.php">View Enrollment Info</a></li>
                <li><a href="UserInfo.php">View User Info</a></li>
                 <li><a href="DropDowns.php">Drop Down Test Page</a></li>
            </ul>
        </div>
        
        <div id="enrollmentCount"><?php
$total_enrollments = count($enrollment_results);
echo "<div class=\"userCountClass\" >";
echo $total_enrollments;
echo "</div>";?></div>
        <div id="viewInfo">
            
<?php

print gettype($enrollment_results); 
foreach($enrollment_results as $key) {
  $er = $enrollment_results[$key];
  $course_id = $er['course_id'];
  $user_name = $er['user']['name'];
   $user_id = $er['user']['id'];
    $enrollment_type = $er['type'];
    $enrollment_state = $er['enrollment_state'];
    $create_date = $er['updated_at'];
    echo "<div class=\"userClass\" >";
    echo "Course_Id: $course_id <br/>";
    echo "Name: $user_name <br/>";
    echo "UserId: $user_id  <br/>";
   echo "Created on: $create_date  <br/>";
    echo "Enrollment Type: $enrollment_type  <br/>";
    echo "Enrollment State: $enrollment_state  <br/>";
    echo "</div>";
}
?></div>
    </body>
</html>
