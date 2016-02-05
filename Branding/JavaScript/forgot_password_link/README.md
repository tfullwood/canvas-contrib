This script uses Javascript to modify a link on the login page to redirect your users to the forgot password form instead of the login form.

There are a couple use cases for this script.

If you would like to include the forgot password link on your institution's website. Use the forgot-password-link.js script.

This script can be useful for institutions that are new to Canvas and using Canvas authentication. You can either create temporary passwords for your users using SIS imports or instruct your students to create their own passwords.

Instructing students to click on the forgot password link to create a password is not always obvious. The create-password-link.js file will redirect users to the forgot password form and tailor the instructional text on the page to new users creating a password.

After the JavaScript has been added to your instance of Canvas you can use the following links to reach the forgot password form.

forgot-password-link.js

```
https://school.instructure.com/login/canvas?forgot_password=1
```

create-password-link.js

```
https://school.instructure.com/login/canvas?create_password=1
```