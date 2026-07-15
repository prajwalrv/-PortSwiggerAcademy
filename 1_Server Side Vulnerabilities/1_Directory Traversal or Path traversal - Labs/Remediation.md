----------------------------------------------------------------------------------------------------------------------------
                                           REMEDIATION
----------------------------------------------------------------------------------------------------------------------------

How to prevent a path traversal attack

The most effective way to prevent path traversal vulnerabilities is to avoid passing user-supplied input to filesystem APIs altogether. Many application functions that do this can be rewritten to deliver the same behavior in a safer way.

If you can't avoid passing user-supplied input to filesystem APIs, we recommend using two layers of defense to prevent attacks:

    Validate the user input before processing it. Ideally, compare the user input with a whitelist of permitted values. If that isn't possible, verify that the input contains only permitted content, such as alphanumeric characters only.
    After validating the supplied input, append the input to the base directory and use a platform filesystem API to canonicalize the path. Verify that the canonicalized path starts with the expected base directory.

Below is an example of some simple php code to validate the canonical path of a file based on user input:

----------------------------------------------------------------------------------------------------------------------------
                                           SPOT THE VULNERABILITY
----------------------------------------------------------------------------------------------------------------------------
1 <?php
2 $template = 'blue.php';
3 if (is_set( $_COOKIE['TEMPLATE']))
4     $template = $_COOKIE['TEMPLATE'];
5 include ( "/home/users/phpguru/templates/" .$template );
6 ?>

FINDINGS :
--> Security Warning: Local File Inclusion (LFI)
    This specific code pattern contains a critical security vulnerability. Because it trusts the value of $_COOKIE['TEMPLATE']
    without checking or cleaning it, a malicious user can manipulate their cookie value (e.g., setting it to ../../../../etc/passwd)
    to read sensitive server files or execute unauthorized code.

--> If the directory traversal vulnerability allows you to run commands, then you can get the full code execution on the server (RCE).

REMDIATION : VALIDATE USER INPUT - INPUT SANITIZATION
-->

Code black :
1 <?php
2 // 1. Define a strict whitelist of allowed template files
3 $allowed_templates = [
4   'bue.php',
5   'dashboard.php',
6   'profile.php'
7 ];
8
9 // 2. Set the default fallback template
10 $template = 'bue.php';
11
12 // 3. Validate the cookie exists and matches the allowed whitelist
13 if (isset($_COOKIE['TEMPLATE']) && in_array($_COOKIE['TEMPLATE'], $allowed_templates, true)) {
       $template = $_COOKIE['TEMPLATE'];
14 }
15
16 // 4. Safely include the file
17 include("/home/users/phpguru/templates/" . $template);
18 ?>
