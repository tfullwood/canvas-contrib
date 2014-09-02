# Add Presenter View

**Author:** Developed by David Keiser-Clark (dwk2@williams.edu) for the Office for Information Technology at Williams College

**Follow:** If you have collaborative ideas or want to be notified of changes, please email me.

**GitHub:** [Williams College: canvas_williams_mods](https://github.com/williamscollege/canvas_williams_mods)

## SCREENSHOTS

 - [Add Presenter View](http://www.screencast.com/t/mclVJfL28 "Add Presenter View") (screenshot)

## FEATURES

#### Add Presenter View (zoom main div; hide all other columns)

 - Add Link: Automatically insert a "Presenter View" hyperlink on the right-side of the "breadcrumbs" navigation
 - Zoom: Increase scale of main (center) region to fill browser, wrapping text as needed
 - Rescale: Resize browser to dynamically increase/decrease visible aspect (zoom) ratio of text and images
 - Hide: Display only main (center) div (hide: top, left, right)
 - Hide: Do not display on urls containing '/external_tools/' (LTI iframe apps) as the JS would be prevented from communicating with the iframe
 - Display All: Increase height dynamically to prevent zoomed page from being inappropriately cut off
 - Resolution: Set width to 900px to ensure magnification occurs in our wired classrooms
 - Exit: Easily return to "normal mode" via "exit" button on left side of screen
 - Note: Hidden content remains in the document object model, but is hidden via CSS. This means the page still functions correctly
 - Note: The "Presenter View" hyperlink will appear on the right-side of all pages that contain the breadcrumbs navigation item
 - Works with: All browsers, including mobile browsers (held in horizontal mode)
 - Intended Usage: classroom projector
