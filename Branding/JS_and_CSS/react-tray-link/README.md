This script uses JavaScript to modify react tray components to add an additional "resources" option to the left navigation.

Modify the trayLinks variable to add or remove links on the popup tray. You can also modify the footerContent to add additional information at the bottom of the tray.

Each object in the array will represent a link on the tray. Use the line below to add a new link. Val is the text value that the user will see and key is the link.

```{key: 'http://www.example.com/your-library', val: 'Library'},```

Only edit the following variables. Do not edit anything after line 8

```
var trayLinks = [
    {key: 'http://www.example.com/your-library', val: 'Library'},
    {key: 'http://www.google.com', val: 'Google'},
    {key: 'http://www.example.com/help-desk', val: 'Help Desk'}
];

var footerContent = 'Footer text area. Put whatever you want here.';
```