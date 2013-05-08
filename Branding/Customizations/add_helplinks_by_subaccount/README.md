Add Help Links for Specific Sub-Accounts
=========================================

You may have many online resources, but some that only apply to certain departments/programs/schools. You want to be able to show links in Canvas' help menu that apply to a specific department/program/school and none of the ones that don't. You can use the CSS here to do this.

The basic logic behind it is this: You add all of the help links at the root account level (you can't add help links within sub-accounts). Add CSS in the root account to hide all of the sub-account help links. Then, within each sub-account, use a small CSS block to unhide the applicable help link(s).

**Note**: The `nth-child` psuedo class is supported in all modern browsers, but not in older ones such as IE8. This shouldn't be an issue, as any browser that doesn't support this class also happens to be not supported by Canvas.