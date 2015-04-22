 // self enrollment screen
 if (window.location.pathname.search('enroll')) {
     $('label[for="student_email"]').text("Username");
     $('p:contains("Please enter your email address:")').text("Please enter your Username:");
 }
