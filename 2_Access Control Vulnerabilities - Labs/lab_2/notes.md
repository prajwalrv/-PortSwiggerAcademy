Lab#2 - Broken Acces Control - Unprotected admin functionality - UnPredictable location


Target Goal - FInd the admin pannel & delete the user carlos

Manual PenTest via burpsuite :

    1. Setup burpsuite proxy ip : 127.0.0.1 on port : 8080
    2. Now open burpsuite and go to proxies tab to turn on intercept
    3. So developer made the url un predictable, but if you check on the page source of that webpage there will be a script
       revealing the address as "/admin-ku7xaw" this is the exact path where can access admin page.
    4. now for the get request update the url with this "/admin-ku7xaw" and forward the request to gain access to admin page
    4. you will be loged on to admin page
    5. Now you will see two users delete the user carlos using delete button
        
        URL : GET https://0a7b00ff049c8bc982ba10a200c200a0.web-security-academy.net/admin-ku7xaw HTTP/2 

        Response : status code 200 for both admin page access & deleting user carlos.

Concept : In some cases, sensitive functionality is concealed by giving it a less predictable URL. This is an example of so-called "security by obscurity". However, hiding sensitive functionality does not provide effective access control because users might discover the obfuscated URL in a number of ways.

    Imagine an application that hosts administrative functions at the following URL:
    https://insecure-website.com/administrator-panel-yb556

    This might not be directly guessable by an attacker. However, the application might still leak the URL to users. The URL might be disclosed in JavaScript that constructs the user interface based on the user's role:
    code : 
    <script>
        var isAdmin = false;
        if (isAdmin) {
            ...
            var adminPanelTag = document.createElement('a');
            adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
            adminPanelTag.innerText = 'Admin panel';
            ...
        }
    </script>

    This script adds a link to the user's UI if they are an admin user. However, the script containing the URL is visible to all users regardless of their role. 